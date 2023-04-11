import os
import subprocess
import json
import sys

# Returns stdout for this command
def run_remote_command(ssh, command):

    with subprocess.Popen(ssh + " '" + command + "'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        output, error = process.communicate()
        process.wait()
    return output.decode("utf-8").strip() # not sure if necessary

# Runs root command from /root/go/src/gus-automation
def run_remote_root_command(ssh, command):
    return run_remote_command(ssh, "sudo bash -c \" cd /root/go/src/gus-automation && " + command + "\"")

def get_ssh(user, address):
    return "ssh -A " + user + "@" + address

# From local machine, moves most recent results from root@control to user@control, preps for syncing
def remote_move_results(user, address, config_file_path):
    ssh = get_ssh(user, address)

    # Since results are by date, this gets most recent results
    results = run_remote_root_command(ssh, "ls /root/go/src/gus-automation/results | sort -r | head -n 1")

    print("Most recent results = " + results)

    config_file = open(config_file_path)

    config = json.load(config_file)

    print("user = " + user)

    # need to create results first
    destination_parent_path = "/users/" + user + "/results/"
    destination_path = destination_parent_path + results 

    source_path = config["base_control_experiment_directory"] + "/" + results
    run_remote_root_command(ssh, "mkdir -p " + destination_parent_path) 

    # Checks to see if experiment has been copied (if the directory exists)
    cmd = "[ -d " + destination_path + " ] && echo 'True'"
    direc_exists = run_remote_root_command(ssh, cmd)

    # If the experiment results haven't been copied already, copy them
    if direc_exists != "True":
        print("Directory has not been copied to user@control yet. About to copy...")
        run_remote_root_command(ssh, "cp -r " + source_path + " " + destination_path)



# Syncs results from user@control to local machine
def sync_results(user_at_address):
    print("Syncing results from " + user_at_address + " to local machine..." )
    os.system("mkdir -p results")

    cmd = "rsync -a " + user_at_address +":results/ results/"
    os.system(cmd)

def usage():
    print("Usage: python3 sync_results.py USER@ADDRESS CONFIG_FILE_PATH")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
    else:
        user_at_address = sys.argv[1]
        config_file_path = sys.argv[2]
        
        temp = user_at_address.split("@")
        user = temp[0]
        address = temp[1]

        remote_move_results(user, address, config_file_path)
        sync_results(user_at_address)

