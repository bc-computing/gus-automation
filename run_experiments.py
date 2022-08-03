from run_experiment_test import run_exper
import os
import subprocess
import sys
import time
import json
from update_json import update
from pathlib import Path
from setup_network_delay_test import setup_network_delay

# Replaces fig6 with fig6a fig6b fig6c
def replace_fig6(config_paths):

    last_slash_index = config_paths[0].rfind("/")
    parent_path = config_paths[0][:last_slash_index + 1]

    for config_path in config_paths:
        if "fig6.json" in config_path:
            # remove fig6 
            config_paths.remove(config_path)

            # add fig6a fig6b fig6c
            for x in ["a", "b", "c"]:
                config_paths.append(parent_path + "fig6" + x + ".json")

    return config_paths


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

    # Adjusts for fig6
    config_paths = replace_fig6(config_paths)

    print("Here are config_paths: " , config_paths)

    for config_path in config_paths:

        # adjusts conflict rate
        if "fig6a" in config_path:
            config_path = config_path.replace("6a", "6")
            update(config_path,"conflict_percentage", 2)
        elif "fig6b" in config_path:
            config_path = config_path.replace("6b", "6")
            update(config_path,"conflict_percentage", 10)
        elif "fig6c" in config_path:
            config_path = config_path.replace("6c", "6")
            update(config_path,"conflict_percentage", 25)

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
