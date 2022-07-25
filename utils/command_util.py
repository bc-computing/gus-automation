import os

from utils.remote_util import *

# runs a unix command and returns the output (that would be printed to stdout)
def check_cmd_output(cmd):
   # output = subprocess.check_output(cmd)
   
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    return output.decode("utf-8").strip("\n") 




def get_master_cmd(config, timestamp):
    exp_directory = os.path.join(config['base_remote_experiment_directory'], timestamp);
    if config['replication_protocol'] == "gryff":
        path_to_master_bin = os.path.join(config['remote_bin_directory'], 'gryff', 'master')
    else:
        path_to_master_bin = os.path.join(config['remote_bin_directory'], 'gus-epaxos', 'master')

    master_command = ' '.join([str(x) for x in [path_to_master_bin, '-N', config['number_of_replicas']]])

    stdout_file = os.path.join(exp_directory, 'master-stdout.log')
    stderr_file = os.path.join(exp_directory, 'master-stderr.log')

    master_command = tcsh_redirect_output_to_files(master_command,
                                               stdout_file, stderr_file)
    return master_command


def get_redis_server_cmd(config, timestamp, server_names_to_ips, server_name):
    exp_directory = os.path.join(config['base_remote_experiment_directory'], timestamp)
    server_addr = server_names_to_ips[server_name]

    redis_remote_bin_directory = os.path.join(config['remote_bin_directory'], "redis", "redis-server")
    server_command = "%s --protected-mode no" % redis_remote_bin_directory

    stdout_file = os.path.join(exp_directory, 'redis-server-%s-stdout.log' % server_name)
    stderr_file = os.path.join(exp_directory, 'redis-server-%s-stderr.log' % server_name)

    server_command = tcsh_redirect_output_to_files(server_command,
                                                   stdout_file, stderr_file)
    return server_command

def get_server_cmd(config, timestamp, server_names_to_ips, server_name):
    exp_directory = os.path.join(config['base_remote_experiment_directory'], timestamp)
    if config['replication_protocol'] == "gryff":
        path_to_server_bin = os.path.join(config['remote_bin_directory'], 'gryff', 'server')
    else:
        path_to_server_bin = os.path.join(config['remote_bin_directory'], 'gus-epaxos', 'server')
    server_addr = server_names_to_ips[server_name]
    master_addr = server_names_to_ips[config['server_names'][0]]

    server_command = ' '.join([str(x) for x in [
        path_to_server_bin,
        '-maddr=%s' % master_addr,
        '-addr=%s' % server_addr,
        '-exec=true',
        '-durable=%s' % config['durable']
    ]])

    server_command += " " + get_replication_protocol_args(config['replication_protocol'])

    if config['scale']:
        number_of_replicas = config['number_of_replicas']
        if number_of_replicas == 7:
            server_command += " -readQ=4 -writeQ=5"
        elif number_of_replicas == 9:
            server_command += " -readQ=5 -writeQ=7"
        elif number_of_replicas == 11:
            server_command += " -readQ=6 -writeQ=8"
        else:
            print("ERROR: scale branch should only be run with n = 7, 9, or 11")

    stdout_file = os.path.join(exp_directory, 'server-%s-stdout.log' % server_name)
    stderr_file = os.path.join(exp_directory, 'server-%s-stderr.log' % server_name)

    server_command = tcsh_redirect_output_to_files(server_command,
                                                    stdout_file, stderr_file)
    return server_command

def get_replication_protocol_args(replication_protocol):
    if replication_protocol == "gus":
        return ""
    elif replication_protocol == "epaxos":
        return "-gus=false -e=true"
    elif replication_protocol == "gryff":
        return "-t -proxy -exec=true -dreply=true"
    elif replication_protocol == "giza":
        return "-gus=false -f=true"
    else:
        print("ERROR: unknown replication protocol. Please choose between gus, epaxos, gryff, and giza")
        exit(1)


def get_client_cmd(config, timestamp, server_names_to_ips):
    exp_directory = os.path.join(config['base_remote_experiment_directory'], timestamp);
    if config['replication_protocol'] == "gryff":
        path_to_client_bin = os.path.join(config['remote_bin_directory'], 'gryff', 'client')
    else:
        path_to_client_bin = os.path.join(config['remote_bin_directory'], 'gus-epaxos', 'client')

    master_addr = server_names_to_ips[config['server_names'][0]]

    if config['layered']:
        client_command = ' '.join([str(x) for x in [
            path_to_client_bin,
            '-maddr=%s' % master_addr,
            '-writes=%f' % config['write_percentage'],
            '-c=%d' % config['conflict_percentage'],
            '-T=1', # Number of clients is hardcoded to 1 for layered experiments
            '-size=4000000', # size is hardcoded to 4MB
            '-redis=%d' % config['number_of_replicas']
        ]])
    else:
        client_command = ' '.join([str(x) for x in [
            path_to_client_bin,
            '-maddr=%s' % master_addr,
            '-writes=%f' % config['write_percentage'],
            '-c=%d' % config['conflict_percentage'],
            '-T=%d' % (int(config['clients_per_replica']) * config['number_of_replicas'])
        ]])

        if config['replication_protocol'] == "gryff":
            client_command += " -proxy"

    # Only run client for 3 minutes.
    timeout = "180s"
    client_command = "timeout %s %s" % (timeout, client_command)

    # Run client in the experiment directory.
    client_command = "cd %s && %s" % (exp_directory, client_command)

    stdout_file = os.path.join(exp_directory, 'client-stdout.log')
    stderr_file = os.path.join(exp_directory, 'client-stderr.log')
    client_command = tcsh_redirect_output_to_files(client_command,
                                                   stdout_file, stderr_file)
    return client_command
