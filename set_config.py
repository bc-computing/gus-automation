import os
import sys
import subprocess
from update_json import update
from utils.command_util import check_cmd_output

def set_config(config_file_path):
    # Get logname (this will be cloudlab_user)
    cloudlab_user = check_cmd_output("logname")

    update(config_file_path, "cloudlab_user", cloudlab_user)


    #ls | sort -r | head -n 1

def usage():
    print("Usage: python3 set_config CONFIG_FILE_PATH")

# Option to run this file as a script and manually specify the config name
if __name__:
    if len(sys.argv) != 2:
        usage()
    set_config(sys.argv[1])