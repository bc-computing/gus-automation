import json
import sys
import os
import subprocess
from textwrap import indent

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
