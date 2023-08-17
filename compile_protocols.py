import sys
import os
import json

# recompiles Go code for each protocol, assuming code is in directories at same level as this one (gus-automation)

BASE_PATH = '~/root/go/src'
CONFIG_PATH = 'configs/config.json'

if __name__ == '__main__':

    config_file = open(config_file_path)
    config = json.load(config_file)

    protocol_dirs = [
        config['gus_epaxos_control_src_directory'],
        config['gryff_control_src_directory']
    ]

    for protocol_dir in protocol_dirs:
        os.system(f"sh {BASE_PATH + '/' + protocol_dir  + '/compile.sh'}")