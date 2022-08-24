#!/usr/local/bin/python3

# Command line script to return percentiles and mean for (gus, gryff, and epaxos) experiment results data
# Author: Cole Dumas, August 2022
# Free to use, as is

import json
import numpy as np
import os
import sys
import statistics
from utils.command_util import check_cmd_output
from pathlib import Path
import pprint
from prettytable import PrettyTable


metrics_dir = "metrics"


def get_metrics(options):
    results_data = build_results_data(options)
    metrics = results_data_to_metrics(options, results_data)
    if "onlytputs" in options:
        output_max_tput_only(metrics)
    else:
        output_metrics(options, metrics)


# returns dictionary of options (with values) interpreted from input args
def read_input(args):
    options = {"figs":[], "protocols":[], "percentiles":[]}

    for arg in args[1:]: # skip program name
        # Flags and options
        if arg.startswith("--interval"):
            interval = arg.split("=")[-1]
            if is_float(interval):
                options["interval"] = float(interval)
            else:
                print("Interval not a number")
                usage()
                sys.exit()
        elif arg.startswith("-i"):
            options["interval"] = 1
        elif arg.startswith("--path"):
            options["path"] = arg.split("=")[-1]
        elif arg.startswith("--txt"):
            options["txt"] = True
        elif arg.startswith("--json"):
            options["json"] = True
        elif arg.startswith("--table"):
            options["table"] = True
        elif arg.startswith("--noprint"):
            options["noprint"] = True
        elif arg.startswith("--clear"):
            options["clear"] = True
        elif arg.startswith("--onlytputs"):
            options["onlytputs"] = True
        # figs and protocols are options that form lists
        elif arg.startswith("--fig"):
            options["fig"].append(arg.split("=")[-1]) # error check later to make sure this fig is actually there
        elif arg.startswith("--protocol"):
            options["protocols"].append(arg.split("=")[-1])
        
        
        # Adjust to take discrete multiple numbers
        # Lower and upper bound arguments
        # ADD option for list of discrete percentiles to calculate
        elif is_float(arg):
            arg = float(arg)
            if arg < 0 or arg > 100:
                print("Percentile argument out of range: ", arg)
                usage()
                sys.exit()
            else: 
                options["percentiles"].append(arg)

        else:
            print("Invalid argument: ", arg )
            usage()
            sys.exit(0)

    # Make sure there is at least one percentile passed (or --clear)
    if len(options["percentiles"]) == 0 and "clear" not in options:
        print("No percentile(s) or clear flag specified")
        usage()
        sys.exit(0)
        
    return options

# fills in some missing options to defaults
def fill_in_options(options):
     # sets path to most recent experiment
    if "path" not in options:
        results_dir = "results/"
        experiment = check_cmd_output("ls " +  results_dir + "| sort -r | head -n 1")
        options["experiment"] = experiment
        options["path"] = results_dir + experiment

    # Fills in figs and protocols if empty to all figs and all protocols
    if len(options["figs"]) == 0:
        options["figs"] = os.listdir(options["path"])
    if len(options["protocols"]) == 0:
        options["protocols"] = os.listdir(options["path"] + "/" + options["figs"][0]) # sets protocols to all of the protocols listed under the first fig

    # if only 1 protocol passed (and interval flag specified) then set upperbound to 100
    if len(options["percentiles"]) == 1 and "intervals" in options:
        options["percentiles"].append(100)

    return options


def build_results_data(options):
    parent_path = options["path"]
    results_data = {}

    for fig in options["figs"]:
        results_data[fig] = {}

        path = parent_path + "/" + fig
        if os.path.exists(path):
            protocols = os.listdir(path)

            for protocol in protocols:
                results_data[fig][protocol] = {}

                # for Fig8 protocol is really "PROTOCOL-WRITE_PERCENTAGE"
                dir_path = path + "/" + protocol + "/client"

                files = os.listdir(dir_path)
                for f in files:
                    extract_file_data(fig, protocol, f, dir_path, results_data)

    return results_data


def extract_file_data(fig, protocol, f, dir_path, results_data):
    if "client-st" not in f: # Excludes processing client-stderr and client-stdout
        file_path = dir_path + "/" + f

        file_key = get_file_key(f, file_path)

        file_contents = np.loadtxt(file_path, dtype=float)

        if "tput" in file_key:
            results_data[fig][protocol][file_key] = file_contents[:,2]
        else: # Reads or Writes
            results_data[fig][protocol][file_key] = file_contents[:,1]


# Returns dictionary of {percentile: value ..., mean: } 
def get_stats(options, file_contents):
    stats = {}

    if "interval" in options: 
        lower_bound = min(options["percentiles"])
        upper_bound = max(options["percentiles"]) 

        if upper_bound + options["interval"] <= 100: # plus step to make it inclusive
            upper_bound = upper_bound + options["interval"]


        for p in np.arange(lower_bound, upper_bound, options["interval"]): # Test this more
            stats["p" + str(p)] = np.percentile(file_contents, p)

    else: # discrete percentiles
        for p in options["percentiles"]:
           # print("about to calculate percentile for file_contents = ", file_contents)
            stats["p" + str(p)] = np.percentile(file_contents, p)

    # mean
    stats["mean"] = statistics.mean(file_contents)

    return stats



# Fix how tputs are calculated

def results_data_to_metrics(options, results_data):
    metrics = results_data.copy()

    # Traverse each item in the original 3D dictionary (results_data)
    for fig, fig_val in results_data.items():
        for protocol, protocol_val in fig_val.items():
            total_protocol_data = np.array([])

            for file_key, file_contents in protocol_val.items(): # file_contents here is trimmed down compared to the file_contents in extract_file_data()
                metrics[fig][protocol][file_key] = get_stats(options, file_contents) # percentiles and mean

                if "tput" not in file_key: # add all Reads and Writes to total_protocol_data
                    total_protocol_data = np.concatenate([total_protocol_data, file_contents])

            metrics[fig][protocol]["total_protocol_data"] = get_stats(options, total_protocol_data)

    return metrics


def metrics_table(metrics):
    table = PrettyTable()
    table.field_names = ["Fig", "Protocol", "File", "Metric", "Value"]
    
    for fig, fig_val in metrics.items():
        for protocol, protocol_val in fig_val.items():
            for file_key, file_contents in protocol_val.items(): # file_contents here is trimmed down compared to the file_contents in extract_file_data()
                for metric, metric_val in file_contents.items():
                    table.add_row([fig, protocol, file_key, metric, metrics[fig][protocol][file_key][metric]])

    return table

 

# Deals with printing and saving to files
def output_metrics(options, metrics):
    if "table" in options or "txt" in options:
        table = metrics_table(metrics)

        if "table" in options:
            print(table)
        
        if "txt":
            table.border = False
            with open(metrics_dir + '/' + options["experiment"] + ".txt", 'w+') as w:
                w.write(str(table))

    if "json" in options:
        with open(metrics_dir + '/' + options["experiment"] + ".json", 'w+') as f:
            json.dump(metrics, f, indent=4)

    if "table" not in options and "noprint" not in options:   # only print regular if not printing table
        metrics_json = json.dumps(metrics, indent = 4) 
        print(metrics_json)


def output_max_tput_only(metrics):
    trimmed_metrics = {}
    for fig, fig_val in metrics.items():
        trimmed_metrics[fig] = {}
        for protocol, protocol_val in fig_val.items():
            trimmed_metrics[fig][protocol] = metrics[fig][protocol]["tput"]["p100.0"]

    print(json.dumps(trimmed_metrics))


# Utility / Small Helpers

def clear_metrics_dir():
    for f in os.listdir(metrics_dir):   
        os.remove(os.path.join(metrics_dir, f))


def usage():
    print("\nUsage: python3 client_metrics [--clear] LOWER_BOUND_OR_SINGLE_PERCENTILE [UPPER_BOUND_OR_SECOND_PERCENTILE] [NTH PERCENTILE]... [-i, --interval=INTERVAL_LENGTH]\n[--path=RESULST_DATA_PATH] [--fig=FIG_NAME] [--protocol=PROTOCOL] [--table] [--noprint] [--txt] [--json]")
    print("\n--clear: clears all json and txt files in metrics before writing to any new files\n\n--interval=INTERVAL_LENTGTH: set interval of percentiles calculated between upper and lowerbound\n\t-i: equivalent to --interval==1\n\n--fig:FIG_NAME: include only FIG_NAME\n\tcan be listed multple times\n\n--protocol=PROTOCOL: only include protocol\n\tcan be listed multiple times\n\n--table: prints metrics in table format\n\n--noprint: no printing  \n\n--txt: saves metrics to text file under client_metrics/\n\n--json: saves metrics to json file under client_metrics/")
    print("\n Many discrete percentile values can be passed. All but max and min are ignored when interval flag is set. \n**If UPPER_BOUND is undefined and --interval is set, then UPPER_BOUND=100\n")


# Gets file_key for results_data dict
def get_file_key(f, file_path):
    if "tput" in f:
        return "tput"
    else:
        return file_path.replace(".txt", "").split("lat")[-1] # adds 'READ_OR_WRITE_OR_TPUT' to results_data dict, removes .txt"

def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    options = fill_in_options(read_input(sys.argv))

    # operate on clear flag (if it's there)
    if "clear" in options:
        clear_metrics_dir()

    get_metrics(options)
