import json
import sys
import concurrent.futures
from setup_nodes import setup_nodes
from run_experiment import run_experiment

from setup_network_delay import get_server_name_to_internal_ip_map

def run_exper(results_extension, config_file_path):
    
    print("About to  run experiment")
    config_file = open(config_file_path)
    config = json.load(config_file)

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:

        timestamp = setup_nodes(config, executor, results_extension)

        # results_extension is timestamp; if the function is called as a script we use timestamp for results folder name
        if results_extension == None:
            results_extension = timestamp

        server_names_to_internal_ips = get_server_name_to_internal_ip_map(config)
        run_experiment(server_names_to_internal_ips, config, results_extension, executor)

    config_file.close()


    


# This function can be called as a script to run one single experiment
# python run_experiment_test <config_file>
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python3 %s <config_file>\n' % sys.argv[0])
        sys.exit(1)

    run_exper(results_extension=None, config_file_path=sys.argv[1])