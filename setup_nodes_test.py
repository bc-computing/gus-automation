import json
import sys
import concurrent.futures
from setup_nodes import setup_nodes

if len(sys.argv) != 2:
    sys.stderr.write('Usage: python3 %s <config_file>\n' % sys.argv[0])
    sys.exit(1)

config_file = open(sys.argv[1])
config = json.load(config_file)

with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
    print(setup_nodes(config, executor).result())

config_file.close()