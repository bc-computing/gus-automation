import concurrent
import os

import time

from utils.command_util import *
from utils.remote_util import *
from setup_network_delay import setup_delays, get_server_name_to_internal_ip_map
from setup_nodes import setup_nodes


def run_experiment(server_names_to_internal_ips, config, timestamp, executor):
    if config['layered']:
        run_layered_experiment(server_names_to_internal_ips, config, timestamp, executor)
    else:
        run_standard_experiment(server_names_to_internal_ips, config, timestamp, executor)

def run_layered_experiment(server_names_to_internal_ips, config, timestamp, executor):
    print("killing machines for safety")
    kill_layered_machines(config, executor)

    print("starting redis servers")
    redis_server_threads = start_redis_servers(config, timestamp, server_names_to_internal_ips)

    print("starting metadata servers")
    master_thread = start_master(config, timestamp)
    server_threads = start_metadata_servers(config, timestamp, server_names_to_internal_ips)
    client_thread = start_clients(config, timestamp, server_names_to_internal_ips)

    print('waiting for client to finish')
    client_thread.wait()

    print("killing master, metadata servers, and redis servers")
    kill_layered_machines(config, executor)

    print("collecting experiment data")
    path_to_client_data = collect_exp_data(config, timestamp, executor)
    # calculate_exp_data(config, path_to_client_data)


def kill_layered_machines(config, executor):
    futures = []

    server_names = config['server_names']
    for i in range(len(server_names)):
        server_url = get_machine_url(config, server_names[i])
        if i < 3:
            futures.append(executor.submit(run_remote_command_sync('killall -9 server', server_url)))
        futures.append(executor.submit(run_remote_command_sync('killall -9 redis-server', server_url)))

    concurrent.futures.wait(futures)


def start_redis_servers(config, timestamp, server_names_to_internal_ips):
    redis_server_threads = []

    redis_servers_started = 0

    for redis_server_name in config['server_names']:
        if redis_servers_started >= config['number_of_replicas']:
            break

        redis_server_url = get_machine_url(config, redis_server_name)
        redis_server_command = get_redis_server_cmd(config, timestamp, server_names_to_internal_ips, redis_server_name)
        redis_server_threads.append(run_remote_command_async(redis_server_command, redis_server_url))

        redis_servers_started += 1

    # I assume there is no way we can detect when the servers are initialized.
    time.sleep(5)
    return redis_server_threads


def start_metadata_servers(config, timestamp, server_names_to_internal_ips):
    metadata_server_threads = []

    metadata_servers_started = 0

    for metadata_server_name in config['server_names']:
        if metadata_servers_started >= 3:
            break

        metadata_server_url = get_machine_url(config, metadata_server_name)
        metadata_server_command = get_server_cmd(config, timestamp, server_names_to_internal_ips, metadata_server_name)
        metadata_server_threads.append(run_remote_command_async(metadata_server_command, metadata_server_url))

        metadata_servers_started += 1

    # I assume there is no way we can detect when the servers are initialized.
    time.sleep(5)
    return metadata_server_threads


def run_standard_experiment(server_names_to_internal_ips, config, timestamp, executor):
    print("killing machines for safety")
    kill_machines(config, executor)

    print("starting machines")
    master_thread = start_master(config, timestamp)
    server_threads = start_servers(config, timestamp, server_names_to_internal_ips)
    client_thread = start_clients(config, timestamp, server_names_to_internal_ips)

    print('waiting for client to finish')
    client_thread.wait()

    print("killing master and server")
    kill_machines(config, executor)

    print("collecting experiment data")
    path_to_client_data = collect_exp_data(config, timestamp, executor)
    # calculate_exp_data(config, path_to_client_data)


def kill_machines(config, executor):
    futures = []

    master_url = get_machine_url(config, config['server_names'][0])
    futures.append(executor.submit(run_remote_command_sync('killall -9 master', master_url)))

    for server_name in config['server_names']:
        server_url = get_machine_url(config, server_name)
        futures.append(executor.submit(run_remote_command_sync('killall -9 server', server_url)))

    concurrent.futures.wait(futures)


def start_master(config, timestamp):
    master_command = get_master_cmd(config, timestamp)
    # The first server listed in the 'server_names' config is the master server.
    master_url = get_machine_url(config, config['server_names'][0])
    time.sleep(5)

    return run_remote_command_async(master_command, master_url)


def start_servers(config, timestamp, server_names_to_internal_ips):
    server_threads = []

    servers_started = 0

    for server_name in config['server_names']:
        if servers_started >= config['number_of_replicas']:
            break

        server_url = get_machine_url(config, server_name)
        server_command = get_server_cmd(config, timestamp, server_names_to_internal_ips, server_name)
        server_threads.append(run_remote_command_async(server_command, server_url))

        servers_started += 1

    # I assume there is no way we can detect when the servers are initialized.
    time.sleep(5)
    return server_threads


def start_clients(config, timestamp, server_names_to_internal_ips):
    # Client machine is colocated with first metadata server in layered experiments
    if config['layered']:
        client_url = get_machine_url(config, config['server_names'][0])
    else:
        client_url = get_machine_url(config, 'client')

    client_command = get_client_cmd(config, timestamp, server_names_to_internal_ips)
    return run_remote_command_async(client_command, client_url)


def collect_exp_data(config, timestamp, executor):
    download_futures = []
    control_exp_directory = os.path.join(config['base_control_experiment_directory'], timestamp)
    remote_exp_directory = os.path.join(config['base_remote_experiment_directory'], timestamp)

    # Master machine data is in the logs of the first server.
    for server_name in config['server_names']:
        server_url = get_machine_url(config, server_name)
        download_futures.append(executor.submit(copy_remote_directory_to_local,
                                                os.path.join(control_exp_directory, 'server-%s' % server_name),
                                                server_url, remote_exp_directory))

    client_url = get_machine_url(config, 'client')
    path_to_client_data = os.path.join(control_exp_directory, 'client')
    download_futures.append(
        executor.submit(copy_remote_directory_to_local, os.path.join(control_exp_directory, 'client'), client_url,
                        remote_exp_directory))

    concurrent.futures.wait(download_futures)

    return path_to_client_data


def calculate_exp_data(config, path_to_client_data):
    # TODO
    client_cdf_analysis_script = os.path.join(config['gus_epaxos_control_src_directory'], "client_metrics.py")
    subprocess.call(["python3.8", client_cdf_analysis_script], cwd=path_to_client_data)
