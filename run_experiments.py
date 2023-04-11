from run_experiment import run_experiment
import os
import subprocess
import sys
import time
import json
from update_json import update
from pathlib import Path
from setup_network_delay_test import setup_network_delay
from set_config import set_config

######### Main Script for running the experiments.  #################
# This will call all of the other scripts/function that setup nodes, 
# add latency and adjust configs.
####################################################################

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

    config_paths = sys.argv[1:]
    
    # Adjusts for fig5
    config_paths = replace_fig5(config_paths)

    print("Here are config_paths: " , config_paths)

    # Need to adjust for figure 11 and figure 8 which just runs gus, but changes n ( =3, =5, =7, =9)
    for config_path in config_paths:

        # adjust user name
        set_config(config_path)

        # adjusts conflict rate - NEED TO FIX PATHING - fig5a not showing up
        if "fig5a" in config_path:
            update(config_path,"conflict_percentage", 2)
        elif "fig5b" in config_path:
            update(config_path,"conflict_percentage", 10)
        elif "fig5c" in config_path:
            update(config_path,"conflict_percentage", 25)

        # default is all protocols
        protocols = ["gus", "epaxos", "gryff"]
        # Figs 8 and 9 plotting is combined gus and giza only
        if "fig9" in config_path or "fig8" in config_path:
            protocols = ["gus", "giza"]

        # Fig 11 and 8 is just gus
        if "fig11" in config_path:
            protocols = ["gus"]
          
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

                    # For fig7, now results file structure is: TIMESTAMP/FIG7/PROTOCOL-WRITE_PERCENTAGE/CLIENT/...
                    results_extension_fig7 = Path(str(results_extension)  + "-" +(str(wr)))

                    setup_network_delay(config_path)
                    run_experiment(results_extension_fig7, config_path)

            
            # This is the Cloudlab experiment that should really be run with 3 and 5 replicas
            elif "fig8n5.json" in config_path:

                num_replicas = [3,5]

                for n in num_replicas:
                    update(config_path, "number_of_replicas", n)

                    # For fig 8, now results file stricture is: TIMESTAMP/FIG8/PROTOCOL-NUM_REPLICAS/CLIENT/...
                    results_extension_fig8 = Path(str(results_extension)  + "-" +(str(n)))

                    setup_network_delay(config_path)
                    run_experiment(results_extension_fig8, config_path)
            
            # For fig8 and fig11 This is the Cloudlab experiment that should really be run with 7 and 9 replicas
            elif "fig8" in config_path or "fig11" in config_path:
                num_replicas = [7,9]

                for n in num_replicas:
                    update(config_path, "number_of_replicas", n)

                    # For fig 8 or fig 11, now results file stricture is: TIMESTAMP/FIG#/PROTOCOL-NUM_REPLICAS/CLIENT/...
                    results_extension_add = Path(str(results_extension)  + "-" +(str(n)))

                    setup_network_delay(config_path)
                    run_experiment(results_extension_add, config_path)
            
            # for fig9, data size is altered between trials
            elif "fig9" in config_path:
                sizes = [4000, 40000, 400000, 4000000] # size of data packets in MB

                for size in sizes:
                    update(config_path, "size", size)

                    # For fig9, now results file structure is TIMESTAMP/FIG9/PROTOCL-size/Client ...
                    results_extension_add = Path(str(results_extension)  + "-" +(str(size)))

                    setup_network_delay(config_path)
                    run_experiment(results_extension_add, config_path)
            
                

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
