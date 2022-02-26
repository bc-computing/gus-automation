import concurrent
import sys

import utils.remote_util

# You may see the error message "RTNETLINK answers: No such file or directory" while this script is running. This
# occurs because we always try to delete any existing tc profiles before configuring our own. If there is no preexisting
# tc profile, then the message will appear, which is fine and will not affect the results of the scripts.

def setup_delays(config, executor):
    # This function trades off performance for simplicity. each helper function takes a copy of the config
    # dictionary rather than passing the necessary config fields in manually.
    # Especially since delays are being setup on each server in parallel, this might increase RAM usage a bit due to
    # all of the copies of the config file.
    futures = []

    server_names_to_ips = get_server_name_to_internal_ip_map(config)
    print("server_names_to_ips:", server_names_to_ips)

    for server_name in config['server_names']:
        server_url = utils.remote_util.get_machine_url(config, server_name)
        print("setting up delay for", server_url)

        server_ips_to_delays = get_ip_to_delay(config, server_names_to_ips, server_name)
        print("ips to delays:", server_ips_to_delays)

        server_interface = get_exp_net_interface(config, server_url)
        if config['emulate_wan_latency']:
            futures.append(executor.submit(add_delays_for_ips, config, server_ips_to_delays,
                                           server_interface, server_url))
        # Get rid of network delay if using lan latency.
        else:
            futures.append(executor.submit(utils.remote_util.run_remote_command_sync,
                                           'sudo tc qdisc del dev %s root' % server_interface,
                                           config['cloudlab_user'], server_url))

    concurrent.futures.wait(futures)
    return server_ips_to_delays


def get_server_name_to_internal_ip_map(config):
    # We get ips through the first server in the server names list just in case the control machine is not in the
    # cloudlab cluster.
    name_to_ip = {}

    for server_name in config['server_names']:
        ip = get_ip_for_server_name_from_remote_machine(server_name,
                                                        utils.remote_util.get_machine_url(config,
                                                                                          config['server_names'][0]))
        name_to_ip[server_name] = ip

    return name_to_ip

def get_ip_for_server_name_from_remote_machine(server_name, remote_url):
    return utils.remote_util.run_remote_command_sync('getent hosts %s | awk \'{ print $1 }\'' % server_name, remote_url).rstrip()


def get_ip_to_delay(config, name_to_ip, server_name):
    ip_to_delay = {}
    name_to_delay = config['server_ping_latencies'][server_name]

    for name, ip in name_to_ip.items():
        if name not in name_to_delay:
            print("ERROR: in the config file, server_names does not match with server_ping_latencies, "
                  "specifically key %s in server_ping_latencies" % server_name)
            sys.exit()
        ip_to_delay[ip] = name_to_delay[name]

    return ip_to_delay


def get_exp_net_interface(config, remote_url):
    return utils.remote_util.run_remote_command_sync('cat /var/emulab/boot/ifmap | awk \'{ print $1 }\'', remote_url).rstrip()


def add_delays_for_ips(config, ip_to_delay, interface, remote_url):
    max_bandwidth = config['max_bandwidth']

    command = 'sudo tc qdisc del dev %s root; ' % interface
    command += 'sudo tc qdisc add dev %s root handle 1: htb; ' % interface
    command += 'sudo tc class add dev %s parent 1: classid 1:1 htb rate %s; ' % (interface, max_bandwidth) # we want unlimited bandwidth
    idx = 2
    for ip, delay in ip_to_delay.items():
        command += 'sudo tc class add dev %s parent 1:1 classid 1:%d htb rate %s; ' % (interface, idx, max_bandwidth)
        command += 'sudo tc qdisc add dev %s handle %d: parent 1:%d netem delay %dms; ' % (interface, idx, idx, delay / 2)
        command += 'sudo tc filter add dev %s pref %d protocol ip u32 match ip dst %s flowid 1:%d; ' % (interface, idx, ip, idx)
        idx += 1
    utils.remote_util.run_remote_command_sync(command, remote_url)