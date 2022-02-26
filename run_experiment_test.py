import json
import sys
import concurrent.futures
from setup_nodes import setup_nodes
from run_experiment import run_experiment

from setup_network_delay import get_server_name_to_internal_ip_map

if len(sys.argv) != 2:
    sys.stderr.write('Usage: python3 %s <config_file>\n' % sys.argv[0])
    sys.exit(1)

config_file = open(sys.argv[1])
config = json.load(config_file)

with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
    timestamp = setup_nodes(config, executor)
    server_names_to_internal_ips = get_server_name_to_internal_ip_map(config)
    run_experiment(server_names_to_internal_ips, config, timestamp, executor)

config_file.close()
