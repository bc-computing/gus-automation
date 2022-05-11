import json
import sys
import concurrent.futures
from setup_network_delay import setup_delays

# config_file_path is relative path
def setup_network_delay(config_file_path):  
    config_file = open(config_file_path)
    config = json.load(config_file)

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        setup_delays(config, executor)
        
    config_file.close() 



if __name__=="__main__":
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python3 %s <config_file>\n' % sys.argv[0])
        sys.exit(1)

    setup_network_delay(sys.argv[1])
    