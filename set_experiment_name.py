from update_json import update
import os
import sys

def set_experiment_name(name):
    # Assumes all config files are in config dir
    configs = os.listdir("configs")

    for config in configs:
        path = "configs/" + config
        update(path, "experiment_name", name)
    
def usage():
    print("Usage: python3 set_experiment_name.py NEW_NAME")

if __name__ == "__main__":

    if len(sys.argv) != 2:
        usage()
    else:
        set_experiment_name(sys.argv[1])