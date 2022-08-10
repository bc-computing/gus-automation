from folder_to_norm_latencies import extract_norm_latencies
from extract_latencies import extract_latencies
from latencies_to_csv import latencies_to_csv
from csvs_to_plot import data_size_latencies_csvs_to_plot, cdf_csvs_to_plot
import os
from pathlib import Path
import sys
import subprocess


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
            case "fig6a":
                print("Plotting fig6a...")
                plot_fig6(plot_target_directory, csv_target_directory, "6a", latencies_folder_paths["gryff"], latencies_folder_paths["gus"], latencies_folder_paths["epaxos"])
            case "fig6b":
                print("Plotting fig6b...")
                plot_fig6(plot_target_directory, csv_target_directory, "6b", latencies_folder_paths["gryff"], latencies_folder_paths["gus"], latencies_folder_paths["epaxos"])
            case "fig6c":
                print("Plotting fig6c...")
                plot_fig6(plot_target_directory, csv_target_directory, "6c", latencies_folder_paths["gryff"], latencies_folder_paths["gus"], latencies_folder_paths["epaxos"])
            case "fig7":
                print("Plotting fig7...")
                plot_fig7(plot_target_directory, csv_target_directory, latencies_folder_paths["gryff"], latencies_folder_paths["gus"], latencies_folder_paths["epaxos"])
            case "fig8":
                print("Still need to implement")
            case "fig9":
                print("Still need to implement")
            case "fig10":
                print("Still need to implement")
            case "fig11":
                print("Plotting fig11...")
                print("latencies_folder_paths[gryff] = ", latencies_folder_paths["gryff"])
                plot_fig11(plot_target_directory, csv_target_directory, latencies_folder_paths["gryff"], latencies_folder_paths["gus"], latencies_folder_paths["epaxos"])
            case _ :
                print("Default reached, Case not found")


def plot_fig7(plot_target_directory, csv_target_directory, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder):
    # gryff_fig_csvs, gus_fig_csvs, epaxos_fig_csvs = calculate_fig_7_csvs(csv_target_directory, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder)
    read_csvs, write_csvs, _, _ = calculate_csvs2("7", csv_target_directory, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder)

    # Reads
    cdf_csvs_to_plot(plot_target_directory, "7", read_csvs["gryff"], read_csvs["gus"], read_csvs["epaxos"], is_for_reads=True)

    # Writes
    cdf_csvs_to_plot(plot_target_directory, "7" + "-write", write_csvs["gryff"], write_csvs["gus"], write_csvs["epaxos"], is_for_reads=False)    


def plot_fig6(plot_target_directory, csv_target_directory, figure_name, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder):
  
    read_csvs, write_csvs, _, _ = calculate_csvs2(figure_name, csv_target_directory, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder)
   
    cdf_csvs_to_plot(plot_target_directory, figure_name, read_csvs["gryff"], read_csvs["gus"], read_csvs["epaxos"],is_for_reads=True )
    cdf_csvs_to_plot(plot_target_directory, figure_name + "-write", write_csvs["gryff"], write_csvs["gus"], write_csvs["epaxos"],is_for_reads=False )

# Plots log scale writes only
def plot_fig11(plot_target_directory, csv_target_directory, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder):
    print("gus_latency_folder: ", gus_latency_folder)
    _ , _, _, write_log_csvs = calculate_csvs2("11", csv_target_directory, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder)

    # Writes 
    print("gus: ", write_log_csvs["gus"])
    print("epaxos: ", write_log_csvs["epaxos"])
    print("gryff: ", write_log_csvs["gryff"])
    cdf_csvs_to_plot(plot_target_directory, "11-write-log", write_log_csvs["gryff"], write_log_csvs["gus"], write_log_csvs["epaxos"], is_for_reads=False, log=True )


def main():
    # Note: folders must be absolute file paths. - CHECK to see if relative paths work
    plot_target_directory = Path("C:/Users/cadum/DistributedSystemsResearch/gus-automation/plotFigs/plots")
    csv_target_directory = Path("C:/Users/cadum/DistributedSystemsResearch/gus-automation/plotFigs/csvs")
    latency_folder = Path("C:/Users/cadum/DistributedSystemsResearch/gus-automation/plotFigs/latencies")

    # Calculated automatically.
    gryff_latency_folder = os.path.join(latency_folder, "gryff")
    gryff_6a_latency_folder = os.path.join(gryff_latency_folder, "6a")
    gryff_6b_latency_folder = os.path.join(gryff_latency_folder, "6b")
    gryff_6c_latency_folder = os.path.join(gryff_latency_folder, "6c")
    gryff_7_latency_folder = os.path.join(gryff_latency_folder, "7")
    gryff_11_latency_folder = os.path.join(gryff_latency_folder, "11")

    gus_latency_folder = os.path.join(latency_folder, "gus")
    gus_6a_latency_folder = os.path.join(gus_latency_folder, "6a")
    gus_6b_latency_folder = os.path.join(gus_latency_folder, "6b")
    gus_6c_latency_folder = os.path.join(gus_latency_folder, "6c")
    gus_7_latency_folder = os.path.join(gus_latency_folder, "7")
    gus_11_latency_folder = os.path.join(gus_latency_folder, "11")

    epaxos_latency_folder = os.path.join(latency_folder, "epaxos")
    epaxos_6a_latency_folder = os.path.join(epaxos_latency_folder, "6a")
    epaxos_6b_latency_folder = os.path.join(epaxos_latency_folder, "6b")
    epaxos_6c_latency_folder = os.path.join(epaxos_latency_folder, "6c")
    epaxos_7_latency_folder = os.path.join(epaxos_latency_folder, "7")
    epaxos_11_latency_folder = os.path.join(epaxos_latency_folder, "11")

    #fig 6
    gryff_fig_6_csvs, gus_fig_6_csvs, epaxos_fig_6_csvs = calculate_fig_6_csvs(csv_target_directory,
                                                                               gryff_6a_latency_folder,
                                                                               gryff_6b_latency_folder,
                                                                               gryff_6c_latency_folder,
                                                                               gus_6a_latency_folder,
                                                                               gus_6b_latency_folder,
                                                                               gus_6c_latency_folder,
                                                                               epaxos_6a_latency_folder,
                                                                               epaxos_6b_latency_folder,
                                                                               epaxos_6c_latency_folder)
    print(gryff_fig_6_csvs, gus_fig_6_csvs, epaxos_fig_6_csvs)

    cdf_csvs_to_plot(plot_target_directory, "6a", gryff_fig_6_csvs[0], gus_fig_6_csvs[0], epaxos_fig_6_csvs[0],
                 is_for_reads=True)
    cdf_csvs_to_plot(plot_target_directory, "6a-write", gryff_fig_6_csvs[1], gus_fig_6_csvs[1], epaxos_fig_6_csvs[1],
                 is_for_reads=False)
    cdf_csvs_to_plot(plot_target_directory, "6b", gryff_fig_6_csvs[2], gus_fig_6_csvs[2], epaxos_fig_6_csvs[2],
                 is_for_reads=True)
    cdf_csvs_to_plot(plot_target_directory, "6b-write", gryff_fig_6_csvs[3], gus_fig_6_csvs[3], epaxos_fig_6_csvs[3],
                 is_for_reads=False)
    cdf_csvs_to_plot(plot_target_directory, "6c", gryff_fig_6_csvs[4], gus_fig_6_csvs[4], epaxos_fig_6_csvs[4],
                 is_for_reads=True)
    cdf_csvs_to_plot(plot_target_directory, "6c-write", gryff_fig_6_csvs[5], gus_fig_6_csvs[5], epaxos_fig_6_csvs[5],
                 is_for_reads=False)

    # fig 7
    gryff_fig_7_csvs, gus_fig_7_csvs, epaxos_fig_7_csvs = calculate_fig_7_csvs(csv_target_directory, gryff_7_latency_folder, gus_7_latency_folder, epaxos_7_latency_folder)
    
    cdf_csvs_to_plot(plot_target_directory, "7a", gryff_fig_7_csvs[0], gus_fig_7_csvs[0], epaxos_fig_7_csvs[0],
                 is_for_reads=True)
    cdf_csvs_to_plot(plot_target_directory, "7b", gryff_fig_7_csvs[2], gus_fig_7_csvs[2], epaxos_fig_7_csvs[2],
                 is_for_reads=False)

    # fig 8

    # fig 9
    # write_ratio_throughput_csv_folder = "/Users/zhouaea/Desktop/plotFigs/write_ratio-throughput"
    # gryff_write_ratio_throughput_csv = os.path.join(write_ratio_throughput_csv_folder, "gryff-write_ratio-throughput.csv")
    # gus_write_ratio_throughput_csv = os.path.join(write_ratio_throughput_csv_folder, "gus-write_ratio-throughput.csv")
    # epaxos_write_ratio_throughput_csv = os.path.join(write_ratio_throughput_csv_folder, "epaxos-write_ratio-throughput.csv")
    #
    # write_ratio_throughput_csvs_to_plot(plot_target_directory, gryff_write_ratio_throughput_csv, gus_write_ratio_throughput_csv, epaxos_write_ratio_throughput_csv)

    # fig data size latencies - fig 10
    data_size_latencies_csv_folder = "/Users/zhouaea/Desktop/plotFigs/data_size-latencies"
    gus_data_size_latencies_csv = os.path.join(data_size_latencies_csv_folder, "gus-data_size-latencies.csv")
    giza_data_size_latencies_csv = os.path.join(data_size_latencies_csv_folder, "giza-data_size-latencies.csv")
    
    data_size_latencies_csvs_to_plot(plot_target_directory, gus_data_size_latencies_csv, giza_data_size_latencies_csv)

    # fig 11 - durable 6c
    gryff_fig_11_csvs, gus_fig_11_csvs, epaxos_fig_11_csvs = calculate_fig_11_csvs(csv_target_directory, gryff_11_latency_folder, gus_11_latency_folder, epaxos_11_latency_folder)
    cdf_csvs_to_plot(plot_target_directory, "11", gryff_fig_11_csvs[1], gus_fig_11_csvs[1], epaxos_fig_11_csvs[1],
                 is_for_reads=False, log=True)


# Returns a tuple of tuple of csv paths.
# This is used for figs 6 and 7
def calculate_csvs2(figure_name, csv_target_directory, gryff_latency_folder, gus_latency_folder, epaxos_latency_folder):

    protocols = ["gryff", "gus", "epaxos"]
    folders = {"gryff": gryff_latency_folder, "gus": gus_latency_folder, "epaxos": epaxos_latency_folder}

    write_latencies = {}
    read_latencies = {}

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

 
# Returns a tuple of tuple of csv paths.
# This is figure 6 in the gryff paper except we display cdf for reads and writes instead of reads and reads in log scale.
def calculate_fig_6_csvs(csv_target_directory,
                         gryff_6a_latency_folder, gryff_6b_latency_folder, gryff_6c_latency_folder,
                         gus_6a_latency_folder, gus_6b_latency_folder, gus_6c_latency_folder,
                         epaxos_6a_latency_folder, epaxos_6b_latency_folder, epaxos_6c_latency_folder):
    
    # Extract data in each latency folder. We only need reads for figure 6, no writes.
    gryff_6a_latencies = extract_norm_latencies(gryff_6a_latency_folder, is_for_reads=True)
    gryff_6b_latencies = extract_norm_latencies(gryff_6b_latency_folder, is_for_reads=True)
    gryff_6c_latencies = extract_norm_latencies(gryff_6c_latency_folder, is_for_reads=True)
    gryff_6a_write_latencies = extract_norm_latencies(gryff_6a_latency_folder, is_for_reads=False)
    gryff_6b_write_latencies = extract_norm_latencies(gryff_6b_latency_folder, is_for_reads=False)
    gryff_6c_write_latencies = extract_norm_latencies(gryff_6c_latency_folder, is_for_reads=False)

    gus_6a_latencies = extract_norm_latencies(gus_6a_latency_folder, is_for_reads=True)
    gus_6b_latencies = extract_norm_latencies(gus_6b_latency_folder, is_for_reads=True)
    gus_6c_latencies = extract_norm_latencies(gus_6c_latency_folder, is_for_reads=True)
    gus_6a_write_latencies = extract_norm_latencies(gus_6a_latency_folder, is_for_reads=False)
    gus_6b_write_latencies = extract_norm_latencies(gus_6b_latency_folder, is_for_reads=False)
    gus_6c_write_latencies = extract_norm_latencies(gus_6c_latency_folder, is_for_reads=False)

    epaxos_6a_latencies = extract_norm_latencies(epaxos_6a_latency_folder, is_for_reads=True)
    epaxos_6b_latencies = extract_norm_latencies(epaxos_6b_latency_folder, is_for_reads=True)
    epaxos_6c_latencies = extract_norm_latencies(epaxos_6c_latency_folder, is_for_reads=True)
    epaxos_6a_write_latencies = extract_norm_latencies(epaxos_6a_latency_folder, is_for_reads=False)
    epaxos_6b_write_latencies = extract_norm_latencies(epaxos_6b_latency_folder, is_for_reads=False)
    epaxos_6c_write_latencies = extract_norm_latencies(epaxos_6c_latency_folder, is_for_reads=False)

    # Calculate csvs for each list of latencies.
    gryff_6a_norm_cdf_csv, _ = latencies_to_csv(csv_target_directory, gryff_6a_latencies, "gryff", "6a")
    gryff_6b_norm_cdf_csv, _ = latencies_to_csv(csv_target_directory, gryff_6b_latencies, "gryff", "6b")
    gryff_6c_norm_cdf_csv, _ = latencies_to_csv(csv_target_directory, gryff_6c_latencies, "gryff", "6c")
    gryff_6a_norm_write_cdf_csv, _ = latencies_to_csv(csv_target_directory, gryff_6a_write_latencies, "gryff", "6a-write")
    gryff_6b_norm_write_cdf_csv, _ = latencies_to_csv(csv_target_directory, gryff_6b_write_latencies, "gryff", "6b-write")
    gryff_6c_norm_write_cdf_csv, _ = latencies_to_csv(csv_target_directory, gryff_6c_write_latencies, "gryff", "6c-write")

    gus_6a_norm_cdf_csv, _ = latencies_to_csv(csv_target_directory, gus_6a_latencies, "gus", "6a")
    gus_6b_norm_cdf_csv, _ = latencies_to_csv(csv_target_directory, gus_6b_latencies, "gus", "6b")
    gus_6c_norm_cdf_csv, _ = latencies_to_csv(csv_target_directory, gus_6c_latencies, "gus", "6c")
    gus_6a_norm_write_cdf_csv, _ = latencies_to_csv(csv_target_directory, gus_6a_write_latencies, "gus", "6a-write")
    gus_6b_norm_write_cdf_csv, _ = latencies_to_csv(csv_target_directory, gus_6b_write_latencies, "gus", "6b-write")
    gus_6c_norm_write_cdf_csv, _ = latencies_to_csv(csv_target_directory, gus_6c_write_latencies, "gus", "6c-write")

    epaxos_6a_norm_cdf_csv, _ = latencies_to_csv(csv_target_directory, epaxos_6a_latencies, "epaxos", "6a")
    epaxos_6b_norm_cdf_csv, _ = latencies_to_csv(csv_target_directory, epaxos_6b_latencies, "epaxos", "6b")
    epaxos_6c_norm_cdf_csv, _ = latencies_to_csv(csv_target_directory, epaxos_6c_latencies, "epaxos", "6c")
    epaxos_6a_norm_write_cdf_csv, _ = latencies_to_csv(csv_target_directory, epaxos_6a_write_latencies, "epaxos", "6a-write")
    epaxos_6b_norm_write_cdf_csv, _ = latencies_to_csv(csv_target_directory, epaxos_6b_write_latencies, "epaxos", "6b-write")
    epaxos_6c_norm_write_cdf_csv, _ = latencies_to_csv(csv_target_directory, epaxos_6c_write_latencies, "epaxos", "6c-write")

    # Package csvs into tuples before returning them
    gryff_fig_6_csvs = (gryff_6a_norm_cdf_csv, gryff_6a_norm_write_cdf_csv,
                      gryff_6b_norm_cdf_csv, gryff_6b_norm_write_cdf_csv,
                      gryff_6c_norm_cdf_csv, gryff_6c_norm_write_cdf_csv)

    gus_fig_6_csvs = (gus_6a_norm_cdf_csv, gus_6a_norm_write_cdf_csv,
                      gus_6b_norm_cdf_csv, gus_6b_norm_write_cdf_csv,
                      gus_6c_norm_cdf_csv, gus_6c_norm_write_cdf_csv)

    epaxos_fig_6_csvs = (epaxos_6a_norm_cdf_csv, epaxos_6a_norm_write_cdf_csv,
                         epaxos_6b_norm_cdf_csv, epaxos_6b_norm_write_cdf_csv,
                         epaxos_6c_norm_cdf_csv, epaxos_6c_norm_write_cdf_csv)

    return gryff_fig_6_csvs, gus_fig_6_csvs, epaxos_fig_6_csvs


def calculate_fig_7_csvs(csv_target_directory, gryff_7_latency_folder, gus_7_latency_folder, epaxos_7_latency_folder):
    gryff_7a_latencies = extract_norm_latencies(gryff_7_latency_folder, is_for_reads=True)
    gryff_7b_latencies = extract_norm_latencies(gryff_7_latency_folder, is_for_reads=False)

    gus_7a_latencies = extract_norm_latencies(gus_7_latency_folder, is_for_reads=True)
    gus_7b_latencies = extract_norm_latencies(gus_7_latency_folder, is_for_reads=False)

    epaxos_7a_latencies = extract_norm_latencies(epaxos_7_latency_folder, is_for_reads=True) # a is reads
    epaxos_7b_latencies = extract_norm_latencies(epaxos_7_latency_folder, is_for_reads=False) # b is writes

    # Calculate csvs for each list of latencies.
    gryff_7a_norm_cdf_csv, gryff_7a_norm_log_cdf_csv = latencies_to_csv(csv_target_directory, gryff_7a_latencies, "gryff", "7a")
    gryff_7b_norm_cdf_csv, gryff_7b_norm_log_cdf_csv = latencies_to_csv(csv_target_directory, gryff_7b_latencies, "gryff", "7b")

    gus_7a_norm_cdf_csv, gus_7a_norm_log_cdf_csv = latencies_to_csv(csv_target_directory, gus_7a_latencies, "gus", "7a")
    gus_7b_norm_cdf_csv, gus_7b_norm_log_cdf_csv = latencies_to_csv(csv_target_directory, gus_7b_latencies, "gus", "7b")

    epaxos_7a_norm_cdf_csv, epaxos_7a_norm_log_cdf_csv = latencies_to_csv(csv_target_directory, epaxos_7a_latencies, "epaxos", "7a")
    epaxos_7b_norm_cdf_csv, epaxos_7b_norm_log_cdf_csv = latencies_to_csv(csv_target_directory, epaxos_7b_latencies, "epaxos", "7b")

    # Package csvs into tuples before returning them
    gryff_fig_7_csvs = (gryff_7a_norm_cdf_csv, gryff_7a_norm_log_cdf_csv,
                        gryff_7b_norm_cdf_csv, gryff_7b_norm_log_cdf_csv)

    gus_fig_7_csvs = (gus_7a_norm_cdf_csv, gus_7a_norm_log_cdf_csv,
                        gus_7b_norm_cdf_csv, gus_7b_norm_log_cdf_csv)

    epaxos_fig_7_csvs = (epaxos_7a_norm_cdf_csv, epaxos_7a_norm_log_cdf_csv,
                        epaxos_7b_norm_cdf_csv, epaxos_7b_norm_log_cdf_csv)

    return gryff_fig_7_csvs, gus_fig_7_csvs, epaxos_fig_7_csvs

def calculate_fig_11_csvs(csv_target_directory, gryff_11_latency_folder, gus_11_latency_folder, epaxos_11_latency_folder):
    print(gryff_11_latency_folder)

    gryff_11_latencies = extract_norm_latencies(gryff_11_latency_folder, is_for_reads=False)
    gus_11_latencies = extract_norm_latencies(gus_11_latency_folder, is_for_reads=False)
    epaxos_11_latencies = extract_norm_latencies(epaxos_11_latency_folder, is_for_reads=False)

    print(gryff_11_latencies)
    # Calculate csvs for each list of latencies.
    gryff_11_cdf_csv, gryff_11_log_cdf_csv = latencies_to_csv(csv_target_directory, gryff_11_latencies, "gryff", "11")
    gus_11_cdf_csv, gus_11_log_cdf_csv = latencies_to_csv(csv_target_directory, gus_11_latencies, "gus", "11")
    epaxos_11_cdf_csv, epaxos_11_log_cdf_csv = latencies_to_csv(csv_target_directory, epaxos_11_latencies, "epaxos", "11")

    # Package csvs into tuples before returning them
    gryff_fig_11_csvs = (gryff_11_cdf_csv, gryff_11_log_cdf_csv)
    gus_fig_11_csvs = (gus_11_cdf_csv, gus_11_log_cdf_csv)
    epaxos_fig_11_csvs = (epaxos_11_cdf_csv, epaxos_11_log_cdf_csv)

    return gryff_fig_11_csvs, gus_fig_11_csvs, epaxos_fig_11_csvs

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

    
