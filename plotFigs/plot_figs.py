# This is a hack to get gus data to plot with gryff data derived from gryff repo.


from folder_to_norm_latencies import extract_norm_latencies
from latencies_to_csv import latencies_to_csv
from csvs_to_plot import cdf_csvs_to_plot, write_ratio_throughput_csvs_to_plot, data_size_latencies_csvs_to_plot
import os.path
from pathlib import Path

from client_metrics import get_metrics




def main():
    # Note: folders must be absolute file paths.
    csv_target_directory = Path("C:/Users/cadum/GusResearch/gus-automation/plotFigs/csvs")
    plot_target_directory = Path("C:/Users/cadum/GusResearch/gus-automation/plotFigs/plots")
    latency_folder = Path("C:/Users/cadum/GusResearch/gus-automation/plotFigs/latencies")
   
    # Calculated automatically.
    gryff_latency_folder = latency_folder / "gryff"
    gryff_6a_latency_folder = gryff_latency_folder / "6a"
    gryff_6b_latency_folder = gryff_latency_folder / "6b"
    gryff_6c_latency_folder = gryff_latency_folder / "6c"
    gryff_7_latency_folder = gryff_latency_folder / "7"

    gus_latency_folder =  latency_folder / "gus"
    gus_6a_latency_folder = gus_latency_folder / "6a"
    gus_6b_latency_folder = gus_latency_folder / "6b"
    gus_6c_latency_folder = gus_latency_folder / "6c"
    gus_7_latency_folder = gus_latency_folder / "7"

    epaxos_latency_folder = latency_folder / "epaxos"
    epaxos_6a_latency_folder = epaxos_latency_folder / "6a"
    epaxos_6b_latency_folder = epaxos_latency_folder / "6b"
    epaxos_6c_latency_folder = epaxos_latency_folder / "6c"
    epaxos_7_latency_folder = epaxos_latency_folder / "7"

    stats = get_metrics(epaxos_6a_latency_folder)
    for x in stats:
        print(x, stats[x])
    
    # fig 6
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
    cdf_csvs_to_plot(plot_target_directory, "7b", gryff_fig_7_csvs[1], gus_fig_7_csvs[1], epaxos_fig_7_csvs[1],
                  is_for_reads=False)

    # fig 8

    # fig 9
    # write_ratio_throughput_csv_folder = "/Users/zhouaea/Desktop/plotFigs/write_ratio-throughput"
    # gryff_write_ratio_throughput_csv = write_ratio_throughput_csv_folder, "gryff-write_ratio-throughput.csv")
    # gus_write_ratio_throughput_csv = write_ratio_throughput_csv_folder, "gus-write_ratio-throughput.csv")
    # epaxos_write_ratio_throughput_csv = write_ratio_throughput_csv_folder, "epaxos-write_ratio-throughput.csv")
    #
    # write_ratio_throughput_csvs_to_plot(plot_target_directory, gryff_write_ratio_throughput_csv, gus_write_ratio_throughput_csv, epaxos_write_ratio_throughput_csv)

    # fig 11
   # data_size_latencies_csv_folder = "c/Users/cadum/GusResearch/gus-automation/plotFigs/data_size-latencies"
   # gus_data_size_latencies_csv = data_size_latencies_csv_folder, "gus-data_size-latencies.csv")
   # giza_data_size_latencies_csv = data_size_latencies_csv_folder, "giza-data_size-latencies.csv")

   # data_size_latencies_csvs_to_plot(plot_target_directory, gus_data_size_latencies_csv, giza_data_size_latencies_csv)


# Returns a tuple of tuple of csv paths.
# This is figure 6 in the gryff paper except we display cdf for reads and writes instead of reads and reads in log scale.
def calculate_fig_6_csvs(csv_target_directory,
                         gryff_6a_latency_folder, gryff_6b_latency_folder, gryff_6c_latency_folder,
                         gus_6a_latency_folder, gus_6b_latency_folder, gus_6c_latency_folder,
                         epaxos_6a_latency_folder, epaxos_6b_latency_folder, epaxos_6c_latency_folder):
    # Extract data in each latency folder. We only need reads for figure 6, no writes.
    print(os.path.exists(gryff_6a_latency_folder))

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

# Should this be calculate_fig_7_csvs?? Found as calculate_fig_9_csvs
def calculate_fig_7_csvs(csv_target_directory, gryff_7_latency_folder, gus_7_latency_folder, epaxos_7_latency_folder):
    # Extract data in each latency folder. We only need reads for figure 6, no writes.
    gryff_7a_latencies = extract_norm_latencies(gryff_7_latency_folder, is_for_reads=True)
    gryff_7b_latencies = extract_norm_latencies(gryff_7_latency_folder, is_for_reads=False)

    gus_7a_latencies = extract_norm_latencies(gus_7_latency_folder, is_for_reads=True)
    gus_7b_latencies = extract_norm_latencies(gus_7_latency_folder, is_for_reads=False)

    epaxos_7a_latencies = extract_norm_latencies(epaxos_7_latency_folder, is_for_reads=True)
    epaxos_7b_latencies = extract_norm_latencies(epaxos_7_latency_folder, is_for_reads=False)

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

if __name__ == "__main__":
    main()
