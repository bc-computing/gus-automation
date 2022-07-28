from run_experiment_test import run_exper
import os
import subprocess
import sys
import time
import json
from update_json import update
from pathlib import Path
from setup_network_delay_test import setup_network_delay

def run():
    now_string = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())

    parent_path = Path("/root/go/src/gus-automation/")

    base_config_file = open("configs/config.json")

    base_config = json.load(base_config_file)
    
    results_parent_path = Path(base_config["base_control_experiment_directory"]) / now_string

    # Need to create parent directory before dumping data?

    config_paths = sys.argv[1:]
    
    # default is all protocols
    protocols = ["gus", "epaxos", "gryff"]

    # Still must adjust for fig6 which  has a b c

    for config_path in config_paths:

        # Get final fig name:
        temp = config_path.split("/")[-1].replace(".json", "")
        temp_path = results_parent_path / (temp)

        for protocol in protocols:
            print("\nRunning", protocol, config_path, "...\n")
            update(config_path, "replication_protocol", protocol)

            results_extension = Path(temp_path) / Path(protocol)

            setup_network_delay(config_path)
            run_exper(results_extension, config_path)


# Must be run as:
# python run_n_experiments <config#> <config#> ...
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: python3 run_n_experiments <fig#> <fig#> ...\n' )
        sys.exit(1)
    
    run()
