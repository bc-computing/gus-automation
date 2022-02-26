import json
import sys
import concurrent.futures
from setup_nodes import setup_nodes
from run_experiment import run_experiment

if len(sys.argv) != 2:
    sys.stderr.write('Usage: python3 %s <config_file>\n' % sys.argv[0])
    sys.exit(1)

config_file = open(sys.argv[1])
config = json.load(config_file)

with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
    timestamp = setup_nodes(config, executor)
    run_experiment(config, timestamp, executor)

config_file.close()
