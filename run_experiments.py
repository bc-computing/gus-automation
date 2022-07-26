from run_experiment_test import run_exper
import os
import subprocess
import sys
import time
import json
from update_json import update
from pathlib import Path
from setup_network_delay_test import setup_network_delay

def run_script():
    now_string = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())

    parent_path = Path("/root/go/src/gus-automation/")

    base_config_file = open(parent_path / Path("configs/config.json"))

    base_config = json.load(base_config_file)

    results_parent_path = parent_path / Path(base_config["base_control_experiment_directory"]) / now_string


    # Need to create parent directory before dumping data?

    figs = sys.argv[1:]
    
    # default is all protocols
    protocols = ["gus", "epaxos", "gryff"]

    # fig must just be a #
    for fig in figs:
        temp_path = results_parent_path / ("fig" + fig)

        config_file_path = parent_path / Path("configs/" + ("fig" + fig + ".json"))

        for protocol in protocols:
            print("\nRunning", protocol, fig, "...\n")
            update(config_file_path, "replication_protocol", protocol)

            results_extension = temp_path / protocol

            setup_network_delay(config_file_path)
            run_exper(results_extension, config_file_path)


# Must be run as:
# python run_n_experiments <config#> <config#> ...
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: python3 run_n_experiments <fig#> <fig#> ...\n' )
        sys.exit(1)
    
    run_script()
