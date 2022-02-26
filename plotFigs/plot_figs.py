# This is a hack to get gus data to plot with gryff data derived from gryff repo.

import glob
from latencies_to_csv import latencies_to_csv
from csvs_to_plot import cdf_csvs_to_plot, write_ratio_throughput_csvs_to_plot, data_size_latencies_csvs_to_plot
import os.path
import random


def main():
    # Note: folders must be absolute file paths.
    csv_target_directory = "/Users/zhouaea/Desktop/plotFigs/csvs"
    plot_target_directory = "/Users/zhouaea/Desktop/plotFigs/plots"
    latency_folder = "/Users/zhouaea/Desktop/plotFigs/latencies"

    # Calculated automatically.
    gryff_latency_folder = os.path.join(latency_folder, "gryff")
    gryff_6a_latency_folder = os.path.join(gryff_latency_folder, "6a")
    gryff_6b_latency_folder = os.path.join(gryff_latency_folder, "6b")
    gryff_6c_latency_folder = os.path.join(gryff_latency_folder, "6c")
    gryff_8_latency_folder = os.path.join(gryff_latency_folder, "8")
    gryff_9_latency_folder = os.path.join(gryff_latency_folder, "9")

    gus_latency_folder = os.path.join(latency_folder, "gus")
    gus_6a_latency_folder = os.path.join(gus_latency_folder, "6a")
    gus_6b_latency_folder = os.path.join(gus_latency_folder, "6b")
    gus_6c_latency_folder = os.path.join(gus_latency_folder, "6c")
    gus_8_latency_folder = os.path.join(gus_latency_folder, "8")
    gus_9_latency_folder = os.path.join(gus_latency_folder, "9")

    epaxos_latency_folder = os.path.join(latency_folder, "epaxos")
    epaxos_6a_latency_folder = os.path.join(epaxos_latency_folder, "6a")
    epaxos_6b_latency_folder = os.path.join(epaxos_latency_folder, "6b")
    epaxos_6c_latency_folder = os.path.join(epaxos_latency_folder, "6c")
    epaxos_8_latency_folder = os.path.join(epaxos_latency_folder, "8")
    epaxos_9_latency_folder = os.path.join(epaxos_latency_folder, "9")

    # fig 6
    # gryff_fig_6_csvs, gus_fig_6_csvs, epaxos_fig_6_csvs = calculate_fig_6_csvs(csv_target_directory,
    #                                                                            gryff_6a_latency_folder,
    #                                                                            gryff_6b_latency_folder,
    #                                                                            gryff_6c_latency_folder,
    #                                                                            gus_6a_latency_folder,
    #                                                                            gus_6b_latency_folder,
    #                                                                            gus_6c_latency_folder,
    #                                                                            epaxos_6a_latency_folder,
    #                                                                            epaxos_6b_latency_folder,
    #                                                                            epaxos_6c_latency_folder)
    # print(gryff_fig_6_csvs, gus_fig_6_csvs, epaxos_fig_6_csvs)
    #
    # cdf_csvs_to_plot(plot_target_directory, "6a", gryff_fig_6_csvs[0], gus_fig_6_csvs[0], epaxos_fig_6_csvs[0],
    #              is_for_reads=True)
    # cdf_csvs_to_plot(plot_target_directory, "6a-write", gryff_fig_6_csvs[1], gus_fig_6_csvs[1], epaxos_fig_6_csvs[1],
    #              is_for_reads=False)
    # cdf_csvs_to_plot(plot_target_directory, "6b", gryff_fig_6_csvs[2], gus_fig_6_csvs[2], epaxos_fig_6_csvs[2],
    #              is_for_reads=True)
    # cdf_csvs_to_plot(plot_target_directory, "6b-write", gryff_fig_6_csvs[3], gus_fig_6_csvs[3], epaxos_fig_6_csvs[3],
    #              is_for_reads=False)
    # cdf_csvs_to_plot(plot_target_directory, "6c", gryff_fig_6_csvs[4], gus_fig_6_csvs[4], epaxos_fig_6_csvs[4],
    #              is_for_reads=True)
    # cdf_csvs_to_plot(plot_target_directory, "6c-write", gryff_fig_6_csvs[5], gus_fig_6_csvs[5], epaxos_fig_6_csvs[5],
    #              is_for_reads=False)

    # fig 8
    # gryff_fig_8_csvs, gus_fig_8_csvs, epaxos_fig_8_csvs = calculate_fig_8_csvs(csv_target_directory, gryff_8_latency_folder, gus_8_latency_folder, epaxos_8_latency_folder)
    #
    # cdf_csvs_to_plot(plot_target_directory, "8a", gryff_fig_8_csvs[0], gus_fig_8_csvs[0], epaxos_fig_8_csvs[0],
    #              is_for_reads=True)
    # cdf_csvs_to_plot(plot_target_directory, "8b", gryff_fig_8_csvs[1], gus_fig_8_csvs[1], epaxos_fig_8_csvs[1],
    #              is_for_reads=False)


    # fig 9
    # gryff_fig_9_csvs, gus_fig_9_csvs, epaxos_fig_9_csvs = calculate_fig_9_csvs(csv_target_directory, gryff_9_latency_folder, gus_9_latency_folder, epaxos_9_latency_folder)
    #
    # cdf_csvs_to_plot(plot_target_directory, "9a", gryff_fig_9_csvs[0], gus_fig_9_csvs[0], epaxos_fig_9_csvs[0],
    #              is_for_reads=True)
    # cdf_csvs_to_plot(plot_target_directory, "9a-log", gryff_fig_9_csvs[1], gus_fig_9_csvs[1], epaxos_fig_9_csvs[1],
    #              is_for_reads=True, log=True)
    # cdf_csvs_to_plot(plot_target_directory, "9b", gryff_fig_9_csvs[2], gus_fig_9_csvs[2], epaxos_fig_9_csvs[2],
    #              is_for_reads=False)
    # cdf_csvs_to_plot(plot_target_directory, "9b-log", gryff_fig_9_csvs[3], gus_fig_9_csvs[3], epaxos_fig_9_csvs[3],
    #              is_for_reads=False, log=True)

    # fig 10

    # fig 11
    # write_ratio_throughput_csv_folder = "/Users/zhouaea/Desktop/plotFigs/write_ratio-throughput"
    # gryff_write_ratio_throughput_csv = os.path.join(write_ratio_throughput_csv_folder, "gryff-write_ratio-throughput.csv")
    # gus_write_ratio_throughput_csv = os.path.join(write_ratio_throughput_csv_folder, "gus-write_ratio-throughput.csv")
    # epaxos_write_ratio_throughput_csv = os.path.join(write_ratio_throughput_csv_folder, "epaxos-write_ratio-throughput.csv")
    #
    # write_ratio_throughput_csvs_to_plot(plot_target_directory, gryff_write_ratio_throughput_csv, gus_write_ratio_throughput_csv, epaxos_write_ratio_throughput_csv)

    # fig 12
    data_size_latencies_csv_folder = "/Users/zhouaea/Desktop/plotFigs/data_size-latencies"
    gus_data_size_latencies_csv = os.path.join(data_size_latencies_csv_folder, "gus-data_size-latencies.csv")
    giza_data_size_latencies_csv = os.path.join(data_size_latencies_csv_folder, "giza-data_size-latencies.csv")

    data_size_latencies_csvs_to_plot(plot_target_directory, gus_data_size_latencies_csv, giza_data_size_latencies_csv)


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


def calculate_fig_8_csvs(csv_target_directory, gryff_8_latency_folder, gus_8_latency_folder, epaxos_8_latency_folder):
    # Extract data in each latency folder. We only need reads for figure 6, no writes.
    gryff_8a_latencies = extract_norm_latencies(gryff_8_latency_folder, is_for_reads=True)
    gryff_8b_latencies = extract_norm_latencies(gryff_8_latency_folder, is_for_reads=False)

    gus_8a_latencies = extract_norm_latencies(gus_8_latency_folder, is_for_reads=True)
    gus_8b_latencies = extract_norm_latencies(gus_8_latency_folder, is_for_reads=False)

    epaxos_8a_latencies = extract_norm_latencies(epaxos_8_latency_folder, is_for_reads=True)
    epaxos_8b_latencies = extract_norm_latencies(epaxos_8_latency_folder, is_for_reads=False)

    # Calculate csvs for each list of latencies.
    gryff_8a_norm_cdf_csv, _ = latencies_to_csv(csv_target_directory, gryff_8a_latencies, "gryff", "8a")
    gryff_8b_norm_cdf_csv, _ = latencies_to_csv(csv_target_directory, gryff_8b_latencies, "gryff", "8b")

    gus_8a_norm_cdf_csv, _ = latencies_to_csv(csv_target_directory, gus_8a_latencies, "gus", "8a")
    gus_8b_norm_cdf_csv, _ = latencies_to_csv(csv_target_directory, gus_8b_latencies, "gus", "8b")

    epaxos_8a_norm_cdf_csv, _ = latencies_to_csv(csv_target_directory, epaxos_8a_latencies, "epaxos", "8a")
    epaxos_8b_norm_cdf_csv, _ = latencies_to_csv(csv_target_directory, epaxos_8b_latencies, "epaxos", "8b")

    # Package csvs into tuples before returning them
    gryff_fig_8_csvs = (gryff_8a_norm_cdf_csv, gryff_8b_norm_cdf_csv)

    gus_fig_8_csvs = (gus_8a_norm_cdf_csv, gus_8b_norm_cdf_csv)

    epaxos_fig_8_csvs = (epaxos_8a_norm_cdf_csv, epaxos_8b_norm_cdf_csv)

    return gryff_fig_8_csvs, gus_fig_8_csvs, epaxos_fig_8_csvs

def calculate_fig_9_csvs(csv_target_directory, gryff_9_latency_folder, gus_9_latency_folder, epaxos_9_latency_folder):
    # Extract data in each latency folder. We only need reads for figure 6, no writes.
    gryff_9a_latencies = extract_norm_latencies(gryff_9_latency_folder, is_for_reads=True)
    gryff_9b_latencies = extract_norm_latencies(gryff_9_latency_folder, is_for_reads=False)

    gus_9a_latencies = extract_norm_latencies(gus_9_latency_folder, is_for_reads=True)
    gus_9b_latencies = extract_norm_latencies(gus_9_latency_folder, is_for_reads=False)

    epaxos_9a_latencies = extract_norm_latencies(epaxos_9_latency_folder, is_for_reads=True)
    epaxos_9b_latencies = extract_norm_latencies(epaxos_9_latency_folder, is_for_reads=False)

    # Calculate csvs for each list of latencies.
    gryff_9a_norm_cdf_csv, gryff_9a_norm_log_cdf_csv = latencies_to_csv(csv_target_directory, gryff_9a_latencies, "gryff", "9a")
    gryff_9b_norm_cdf_csv, gryff_9b_norm_log_cdf_csv = latencies_to_csv(csv_target_directory, gryff_9b_latencies, "gryff", "9b")

    gus_9a_norm_cdf_csv, gus_9a_norm_log_cdf_csv = latencies_to_csv(csv_target_directory, gus_9a_latencies, "gus", "9a")
    gus_9b_norm_cdf_csv, gus_9b_norm_log_cdf_csv = latencies_to_csv(csv_target_directory, gus_9b_latencies, "gus", "9b")

    epaxos_9a_norm_cdf_csv, epaxos_9a_norm_log_cdf_csv = latencies_to_csv(csv_target_directory, epaxos_9a_latencies, "epaxos", "9a")
    epaxos_9b_norm_cdf_csv, epaxos_9b_norm_log_cdf_csv = latencies_to_csv(csv_target_directory, epaxos_9b_latencies, "epaxos", "9b")

    # Package csvs into tuples before returning them
    gryff_fig_9_csvs = (gryff_9a_norm_cdf_csv, gryff_9a_norm_log_cdf_csv,
                        gryff_9b_norm_cdf_csv, gryff_9b_norm_log_cdf_csv)

    gus_fig_9_csvs = (gus_9a_norm_cdf_csv, gus_9a_norm_log_cdf_csv,
                        gus_9b_norm_cdf_csv, gus_9b_norm_log_cdf_csv)

    epaxos_fig_9_csvs = (epaxos_9a_norm_cdf_csv, epaxos_9a_norm_log_cdf_csv,
                        epaxos_9b_norm_cdf_csv, epaxos_9b_norm_log_cdf_csv)

    return gryff_fig_9_csvs, gus_fig_9_csvs, epaxos_fig_9_csvs

def extract_norm_latencies(folder, is_for_reads):
    if is_for_reads:
        log_files = glob.glob(os.path.join(folder, "latFileRead*"))
    else:
        log_files = glob.glob(os.path.join(folder, "latFileWrite*"))

    # print(os.path.join(folder, "latFileRead*"))
    # print(log_files)

    norm_latencies = []
    regional_latencies = []
    regional_latency_counts = []

    # Convert regional latencies into a 2D list and count how many operations were recorded in each region.
    for log_file in log_files:
        with open(log_file) as f:
            ops = f.readlines()
            # print("first five ops")
            # print(ops[:5])
            # print("%d ops in this region" % len(ops))
            regional_latencies.append(ops)
            regional_latency_counts.append(len(ops))

    latencies_to_take = min(regional_latency_counts)
    # print("taking %d ops from each region" % latencies_to_take)

    # Sample an equal amount of latencies from each region to "normalize" the data. Only extract the latency field.
    for latencies_in_region in regional_latencies:
        sample = random.sample(latencies_in_region, latencies_to_take)
        # print("first 5 samples that are being added")
        # print(sample[:5])
        latencies_to_add = [float(op.split(" ")[1]) for op in sample]
        # print("first 5 latencies that are being added")
        # print(latencies_to_add[:5])
        norm_latencies += latencies_to_add
    # print("%d latencies collected" % len(norm_latencies))
    # print("first 5 latencies")
    # print(norm_latencies[:5])

    return norm_latencies


# # 49.5 reads, 49.5% writes, and 1.0% rmws with 25% conflicts, plot read and write data n = 3
# def plot_fig_8(plot_config, gryff_8_norm_cdf_csv, gus_8_latency_folder, epaxos_8_latency_folder):
#
# # 49.5 reads, 49.5% writes, and 1.0% rmws with 25% conflicts, plot read and write data. n = 5
# def plot_fig_9(plot_config, gryff_9_norm_cdf_csv, gus_9_latency_folder, epaxos_9_latency_folder):

if __name__ == "__main__":
    main()
