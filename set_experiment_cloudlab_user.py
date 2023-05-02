from update_json import update
import os
import sys

# Goes into config files and adjusts Cloudlab experiment name
def set_experiment_cloudlab_user(cloudlab_user):
    # Assumes all config files are in config dir
    configs = os.listdir("configs")

    for config in configs:
        path = "configs/" + config
        update(path, "cloudlab_user", cloudlab_user)
    
def usage():
    print("Usage: python3 set_experiment_name.py NEW_CLOUDLAB_USER")

if __name__ == "__main__":


    if len(sys.argv) != 2:
        usage()
    else:
        set_experiment_cloudlab_user(sys.argv[1])