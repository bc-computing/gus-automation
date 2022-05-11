import json
import sys
import os
import subprocess

# run via:
# python update_config <config_num> <protocol>

# updates a json file
def update(file_path, key, new_value):
    file = open(file_path, "r+")
    json_object = json.load(file)
    file.close()

    json_object[key] = new_value

    file = open(file_path, "w")
    json.dump(json_object, file, indent=4)
    # file.write(simplej)

    file.close()


def main():
    file_path = "configs/fig" + sys.argv[1] + ".json" 
    print(file_path)
    update(file_path, "replication_protocol", sys.argv[2])



main()