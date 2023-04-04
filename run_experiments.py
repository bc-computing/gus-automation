from run_experiment import run_experiment
import os
import subprocess
import sys
import time
import json
from update_json import update
from pathlib import Path
from setup_network_delay_test import setup_network_delay

# Replaces fig5 with fig5a fig5b fig5c
def replace_fig5(config_paths):

    last_slash_index = config_paths[0].rfind("/")
    parent_path = config_paths[0][:last_slash_index + 1]

    for config_path in config_paths:
        if "fig5.json" in config_path:
            # remove fig5 
            config_paths.remove(config_path)

            # add fig5a fig5b fig5c
            for x in ["a", "b", "c"]:
                config_paths.append(parent_path + "fig5" + x + ".json")

    return config_paths


def run():
    now_string = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())

    parent_path = Path("/root/go/src/gus-automation/")

    base_config_file = open("configs/config.json")

    base_config = json.load(base_config_file)
    
    results_parent_path = Path(base_config["base_control_experiment_directory"]) / now_string

    # Need to create parent directory before dumping data?

    config_paths = sys.argv[1:]
    
    # Adjusts for fig5
    config_paths = replace_fig5(config_paths)

    print("Here are config_paths: " , config_paths)

    # Fig 7 is for each protocol, change throughput 

    # Need to adjust for figure 11 which just runs gus, but changes n ( =3, =5, =7, =9)
    for config_path in config_paths:

        # adjusts conflict rate - NEED TO FIX PATHING - fig5a not showing up
        if "fig5a" in config_path:
            update(config_path,"conflict_percentage", 2)
        elif "fig5b" in config_path:
            update(config_path,"conflict_percentage", 10)
        elif "fig5c" in config_path:
            update(config_path,"conflict_percentage", 25)

        # default is all protocols
        protocols = ["gus", "epaxos", "gryff"]
        # Fig 9 plotting is combined gus and giza only
        if "fig9" in config_path:
            protocols = ["gus", "epaxos"]


        print("Config path = " , config_path)

        # Get final fig name:
        trimmed_fig = config_path.split("/")[-1].replace(".json", "")
        temp_path = results_parent_path / (trimmed_fig)

        for protocol in protocols:
            print("\nRunning", protocol, config_path, "...\n")
            update(config_path, "replication_protocol", protocol)

            results_extension = Path(temp_path) / Path(protocol)
        
            # NOT SURE WHY - Gryff not working 
            # For fig 7 (old fig 9 thought it was fig8), for each protocol, change throughput 
            if "fig7" in trimmed_fig:

                write_percentages = [.1, .3, .5, .7, .9]
                for wr in write_percentages: 
                    update(config_path, "write_percentage", wr)

                    # For fig7, now results file structure is: TIMESTAMP/FIG8/PROTOCOL-WRITE_PERCENTAGE/CLIENT/...
                    results_extension_fig7 = Path(str(results_extension)  + "-" +(str(wr)))

                    setup_network_delay(config_path)
                    run_experiment(results_extension_fig7, config_path)

            else:
                setup_network_delay(config_path)
                run_experiment(results_extension, config_path)


# Must be run as:
# python run_n_experiments <config#> <config#> ...
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: python3 run_n_experiments <fig#> <fig#> ...\n' )
        sys.exit(1)
    
    run()
