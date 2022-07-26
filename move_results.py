from utils.command_util import check_cmd_output
import sys
import os
import json

# moves most recent results from root to cloudlab user directory 

def move_results(config_file_path):
    # Since results are by date, this gets most recent results
    results = check_cmd_output("ls results | sort -r | head -n 1")
    print(results)

    config_file = open(config_file_path)

    config = json.load(config_file)


    # need to create results first
    destination_parent_path = "/users/" + config["cloudlab_user"] + "/results/"
    destination_path = destination_parent_path + results

    source_path = config["base_control_experiment_directory"] + "/" + results
    os.system("mkdir -p " + destination_parent_path) 

   # If the experiment results haven't been copied already, copy them
    if not os.path.exists(destination_path):
            os.system("cp -r " + source_path + " " + destination_path)


# Uses configs/config (just to get results directoriy paths)
def move_results2():
    config_file_path = "configs/config.json"

    # Since results are by date, this gets most recent results
    results = check_cmd_output("ls /root/go/src/gus-automation/results | sort -r | head -n 1")

    print(results)

    config_file = open(config_file_path)

    config = json.load(config_file)

    user = sys.stdin.readline().strip()
    print("user = " + user)

    # need to create results first
    destination_parent_path = "/users/" + user + "/results/"
    destination_path = destination_parent_path + results

    source_path = config["base_control_experiment_directory"] + "/" + results
    print("source_path = " + source_path) 
    os.system("mkdir -p " + destination_parent_path) 
    print("just made dir, destination_parent_path=" + destination_parent_path)

    print("destination_path = " + destination_path)
    print(os.path.exists(destination_path))
   # If the experiment results haven't been copied already, copy them
    if not os.path.exists(destination_path):
        print("About to copy...")
        os.system("cp -r " + source_path + " " + destination_path)


def usage():
    print("Usage: python3 move_results CONFIG_FILE_PATH")

# Option to run this file as a script and manually specify the config name
if __name__:
    if len(sys.argv) != 2:
        usage()
    else:
        move_results2()
