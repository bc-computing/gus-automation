from collections import OrderedDict
import copy
import json
import sys

region_to_country = {
    "af-south-1": "cape town",
    "ap-east-1": "hong kong",
    "ap-northeast-1": "tokyo", # gryff called this tokyo, but its official name on the website is tokyo
    "ap-northeast-2": "seoul",
    "ap-northeast-3": "osaka",
    "ap-south-1": "mumbai",
    "ap-southeast-1": "singapore",
    "ap-southeast-2": "sydney",
    "ca-central-1": "central", # in Canada
    "eu-central-1": "frankfurt",
    "eu-north-1": "stockholm",
    "eu-south-1": "milan",
    "eu-west-1": "ireland",
    "eu-west-2": "london",
    "eu-west-3": "paris",
    "me-south-1": "bahrain",
    "sa-east-1": "são paulo",
    "us-east-1": "virginia", # for some reason the table lists N. Virginia
    "us-east-2": "ohio",
    "us-west-1": "california", # for some reason the table lists N. California
    "us-west-2": "oregon"
}

# Use dictionary above to convert regions to country names to stay consistent with gryff naming conventions.
def convert_region_to_country(all_latencies):
    regions = []
    for region in all_latencies:
        regions.append(region)

    for first_layer in regions:
        for second_layer in regions:
            all_latencies[first_layer][region_to_country[second_layer]] = all_latencies[first_layer].pop(second_layer)
        all_latencies[region_to_country[first_layer]] = all_latencies.pop(first_layer)

# Get rid of unnecessary regions.
def filter_countries(config, all_latencies):
    regions = []
    for region in all_latencies:
        regions.append(region)

    # Ensure all region names are valid
    regions_to_keep = config["server_names"]
    for region_to_keep in regions_to_keep:
        if region_to_keep not in regions:
            print("User error: %s is not a valid country!" % region_to_keep)
            exit()

    # Delete unnecessary regions
    for first_layer in regions:
        if first_layer not in regions_to_keep:
            del all_latencies[first_layer]
        else:
            for second_layer in regions:
                if second_layer not in regions_to_keep:
                    del all_latencies[first_layer][second_layer]



if len(sys.argv) != 2:
    sys.stderr.write('Usage: python3 %s <config_file>\n' % sys.argv[0])
    sys.exit(1)

with open(sys.argv[1]) as config_file:
    config = json.load(config_file, object_pairs_hook=OrderedDict)

all_latencies_file = open("all_latencies.json")
all_latencies = json.load(all_latencies_file)

convert_region_to_country(all_latencies)
# print(all_latencies)
filter_countries(config, all_latencies)
# print(all_latencies)
config["server_ping_latencies"] = all_latencies
with open(sys.argv[1], 'w') as config_file:
    json.dump(config, config_file, indent=2)




