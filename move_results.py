from utils.command_util import check_cmd_output
import sys
import os

# moves most recent results from root to cloudlab user directory 

def move_results(config_file_path):
    # Since results are by date, this gets most recent results
    results = check_cmd_output("ls | sort -r | head -n 1")

    config_file = open(config_file_path)

    config = json.load(config_file)


    # need to create results first
    destination_path = "/users/" + config[cloudlab_user] + "/results/" + results

    source_path = config["base_control_experiment_directory"] + "/" + results 
    os.system("cp-r " + source_path + " " + destination_path)




def usage():
    print("Usage: python3 move_results CONFIG_FILE_PATH")

# Option to run this file as a script and manually specify the config name
if __name__:
    if len(sys.argv) != 2:
        usage()
    set_config(sys.argv[1])