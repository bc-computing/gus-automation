import csv
import numpy
import os


# just takes a list of latencies, does not care about the context of the latencies
def latencies_to_csv(csv_target_directory, latencies, protocol, figure):
    # print("converting latencies to cdfs")
    cdf_data, cdf_log_data = latencies_to_cdfs(latencies)

    # if protocol == "epaxos":
    #     print(protocol, figure, "cdf_data")
    #     print(cdf_data)
    #     exit()

    # print("first five rows for cdf data and first five rows for cdf log data")
    # print(cdf_data[:5], cdf_log_data[:5])

    cdf_csv_file = os.path.join(csv_target_directory, protocol, '%s-%s.csv' % (protocol, figure))
    cdf_log_csv_file = os.path.join(csv_target_directory, protocol, '%s-%s-log.csv' % (protocol, figure))
    # print("cdf file is called %s and log cdf file is called %s" % (cdf_csv_file, cdf_log_csv_file))
    #
    # print("converting cdfs to csvs")
    generate_csv_for_cdf_plot(cdf_csv_file, cdf_data)
    generate_csv_for_cdf_plot(cdf_log_csv_file, cdf_log_data, log=True)
    return cdf_csv_file, cdf_log_csv_file


def latencies_to_cdfs(latencies, cdf_log_precision=4):
    nplatencies = numpy.asarray(latencies)
    cdf_data = calculate_cdf_for_npdata(nplatencies)
    cdf_log_data = calculate_cdf_log_for_npdata(nplatencies, cdf_log_precision)
    return cdf_data, cdf_log_data


# helper for latencies_to_cdfs
def calculate_cdf_for_npdata(npdata):
    ptiles = []
    for i in range(1, 100):  # compute percentiles [1, 100)
        ptiles.append([i, numpy.percentile(npdata, i)])
    return ptiles


# helper for latencies_to_cdfs
def calculate_cdf_log_for_npdata(npdata, precision):
    ptiles = []
    base = 0
    scale = 1
    for i in range(0, precision):
        for j in range(0, 90):
            if i == 0 and j == 0:
                continue
            ptiles.append([base + j / scale, numpy.percentile(npdata, base + j / scale)])
        base += 90 / scale
        scale = scale * 10
    return ptiles


def generate_csv_for_cdf_plot(csv_file, cdf_data, log=False):
    with open(csv_file, 'w+') as f:
        csvwriter = csv.writer(f)
        k = 1
        for i in range(len(cdf_data)):
            data = [cdf_data[i][1], cdf_data[i][0] / 100]
            if log and abs(cdf_data[i][0] / 100 - (1 - 10 ** -k)) < 0.000001:
                data.append(1 - 10 ** -k)
                k += 1
            csvwriter.writerow(data)
