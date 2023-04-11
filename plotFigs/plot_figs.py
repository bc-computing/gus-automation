from folder_to_norm_latencies import extract_norm_latencies
from extract_latencies import extract_latencies
from latencies_to_csv import latencies_to_csv
from csvs_to_plot import cdf_csvs_to_plot, tput_wp_plot
import os
from pathlib import Path
import sys
import subprocess
import json
import numpy as np


# Working on passing a folder for results
# File path has structure: TIMESTAMP / FIG# / PROTOCOL/ CLIENT

# Make sure to run when current wording directory is plot_figs/
def main2(results_path):

    plot_target_directory = Path("plots")
    csv_target_directory = Path("csvs")

    # list all figs in timestap
    figs = os.listdir(results_path)
    for fig in figs:
        fig_path = Path(results_path) / Path(fig)

        protocols = os.listdir(fig_path)
        latencies_folder_paths = {}
        for protocol in protocols:
            latencies_folder_path = fig_path / Path(protocol + "/client")
            latencies_folder_paths[protocol] = latencies_folder_path

        match fig:
            case "fig5a":
                print("Plotting fig5a...")
                plot_fig5(plot_target_directory, csv_target_directory, "5a", latencies_folder_paths["gryff"], latencies_folder_paths["gus"], latencies_folder_paths["epaxos"])
            case "fig5b":
                print("Plotting fig5b...")
                plot_fig5(plot_target_directory, csv_target_directory, "5b", latencies_folder_paths["gryff"], latencies_folder_paths["gus"], latencies_folder_paths["epaxos"])
            case "fig5c":
                print("Plotting fig5c...")
                plot_fig5(plot_target_directory, csv_target_directory, "5c", latencies_folder_paths["gryff"], latencies_folder_paths["gus"], latencies_folder_paths["epaxos"])
            case "fig6":
                print("Plotting fig6...")
                plot_fig6(plot_target_directory, csv_target_directory, latencies_folder_paths["gryff"], latencies_folder_paths["gus"], latencies_folder_paths["epaxos"])
            case "fig7":
                print("Plotting fig7...")
                plot_fig7(plot_target_directory, results_path, csv_target_directory, latencies_folder_paths)
            case "fig8":
                print("separate from automated plotting. Latencies were originanlly manually extracted. Use layered/plot.py")
            case "fig9":
                print("Plot was produced manually through extracting latencies from each sub experiment, finding percentiles and plotting")
            case "fig10":
                print("Plotting fig10...")
                plot_fig10(plot_target_directory, csv_target_directory, latencies_folder_paths["gryff"], latencies_folder_paths["gus"], latencies_folder_paths["epaxos"])
            case "fig11":
                # Old fig12 and fig12 n=5
                print("Seperate from automated plotting. Use scale/scale_plot.py. See README for details") 
            case _ :
                print("Default reached, Plotting Case not found")


def plot_fig6(plot_target_directory, csv_target_directory, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder):
    # gryff_fig_csvs, gus_fig_csvs, epaxos_fig_csvs = calculate_fig_6_csvs(csv_target_directory, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder)
    read_csvs, write_csvs, _, _ = calculate_csvs_cdf("6", csv_target_directory, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder)

    # Reads
    cdf_csvs_to_plot(plot_target_directory, "6", read_csvs, is_for_reads=True)

    # Writes
    cdf_csvs_to_plot(plot_target_directory, "6" + "-write", write_csvs, is_for_reads=False)    


def plot_fig5(plot_target_directory, csv_target_directory, figure_name, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder):
  
    read_csvs, write_csvs, _, _ = calculate_csvs_cdf(figure_name, csv_target_directory, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder)
   
    cdf_csvs_to_plot(plot_target_directory, figure_name, read_csvs,is_for_reads=True )
    cdf_csvs_to_plot(plot_target_directory, figure_name + "-write", write_csvs, is_for_reads=False )

# Plots log scale writes only
def plot_fig10(plot_target_directory, csv_target_directory, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder):
    print("gus_latency_folder: ", gus_latency_folder)
    _ , _, _, write_log_csvs = calculate_csvs_cdf("10", csv_target_directory, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder)

    # Writes 
    cdf_csvs_to_plot(plot_target_directory, "10-write-log", write_log_csvs, is_for_reads=False, log=True )


# fig7 was really fig9 and is now fig7
def plot_fig7(plot_target_directory, results_path, csv_target_directory, latencies_folder_paths):
    # For fig7, now results file structure is: TIMESTAMP/FIG7/PROTOCOL-WRITE_PERCENTAGE/CLIENT/....    
    # latencies_folder_paths = TIMESTAMP/FIG7/PROTOCOL/

    # throughputs is a dictionary of throughputs (lookup via throughputs[protocol][wp])
    throughputs = calculate_tput_wp("7", results_path, csv_target_directory, latencies_folder_paths)
    tput_wp_plot(plot_target_directory, "7", throughputs)


# Need to cut out CSVS too like with fig7
# Returns a tuple of tuple of csv paths.
# This is used for figs 5 , 6 and 10
def calculate_csvs_cdf(figure_name, csv_target_directory, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder):

    print("quick print")
    protocols = ["gryff", "gus", "epaxos"]
    folders = {"gryff": gryff_latency_folder, "gus": gus_latency_folder, "epaxos": epaxos_latency_folder}

    write_latencies = {}
    read_latencies = {}

    write_log_latencies = {}
    read_log_latencies = {}

    for protocol, folder in folders.items(): 
        # Create dictionary of write latencies (one key-value pair per protocol)
        w_latencies = extract_norm_latencies(folder, is_for_reads=False)
        write_latencies[protocol] = w_latencies

         # Create dictionary of read latencies
        r_latencies = extract_norm_latencies(folder, is_for_reads=True)
        read_latencies[protocol] = r_latencies

    print("read latencies: ", len(read_latencies))

    # Protocol : csv
    read_csvs = {}
    write_csvs = {}

    read_log_csvs = {}
    write_log_csvs = {}

    # read 
    for protocol, latency in read_latencies.items():
        norm_cdf_csv, norm_log_cdf_csv=  latencies_to_csv(csv_target_directory, latency, protocol, figure_name)
        read_csvs[protocol] = norm_cdf_csv 
        read_log_csvs[protocol] = norm_log_cdf_csv

    # write
    for protocol, latency in write_latencies.items():
        norm_cdf_csv, norm_log_cdf_csv =  latencies_to_csv(csv_target_directory, latency, protocol, figure_name + "-write")
        write_csvs[protocol] = norm_cdf_csv 
        write_log_csvs[protocol] = norm_log_cdf_csv

    return read_csvs, write_csvs, read_log_csvs, write_log_csvs

# # New idea: Don't write to CSV files, just make Numpy arrays and plot directly
# # calculates thoughput vs write percentage (fig7)
def calculate_tput_wp(figure_name, results_path, csv_target_directory, latencies_folder_paths):
    # ex: gryff_latency_dict contains subfolders with write percentage 
    # should give a dictionary of p100 throughputs (I think this is "maximum attainable througput" as referenced in the NSDI23_GUS paper) with PROTOCOL-WP as key (outer key of fig7)
    raw_throughputs = json.loads(check_cmd_output("python3 ../client_metrics.py 100 --onlytputs --path=" + results_path))["fig" + figure_name]

    # 2D dictionary indexed like: throughputs[PROTOCOL][WRITE_PERCENTAGE]
    throughputs = {}

    for protocol_wp, tput in raw_throughputs.items():

        temp = protocol_wp.split("-")
        protocol = temp[0]
        wp = temp[1]

        if protocol not in throughputs:
            throughputs[protocol] = np.empty([0,2], dtype=float)
        throughputs[protocol] = np.append( throughputs[protocol], [[float(wp), float(tput)]], axis=0) # throughputs[protocl] is a 2D numpy array with the strucutre [write-percentage, tput] on each row


    return throughputs
    
    
# Delete and fix packaging
def check_cmd_output(cmd):
   # output = subprocess.check_output(cmd)
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    return output.decode("utf-8").strip("\n") 


# returns newest results. Assumes results are in ../results
def most_recent_results():
    results_dir = "../results/"
    return results_dir + check_cmd_output("ls " +  results_dir + "| sort -r | head -n 1")


def usage():
    print("Usage: python3 plot_figs.py RESULTS_PATH")

if __name__ == "__main__":
    match len(sys.argv):
        case 1: 
            main2(most_recent_results())
        case 2:
            main2(sys.argv[1])
        case _:
            usage()

    
