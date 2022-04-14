import csv
import json
import numpy
import os

def tempo_json_to_csv(filename, protocol):
    tempo_cdf_data = extract_tempo_latencies(filename)
    csv_file = '%s.csv' % protocol
    generate_csv_for_cdf_plot(csv_file, tempo_cdf_data)
    return csv_file

def extract_tempo_latencies(filename):
    with open(filename) as file:
        data = json.load(file)

    ptiles = []
    for key, value in data['global_client_latency']['hist']['percentiles'].items():
        ptiles.append([key, value / 1000])
    ptiles.sort()
    return ptiles


def gus_latencies_to_csv(latencies, protocol):
    tempo_cdf_data = calculate_gus_percentiles(latencies)
    csv_file = '%s.csv' % protocol
    generate_csv_for_cdf_plot(csv_file, tempo_cdf_data)
    return csv_file

def calculate_gus_percentiles(npdata):
    tempo_ptiles = tempo_ptiles = [0.66, 0.11, 0.93, 0.21, 0.16, 0.84, 0.94, 0.65, 0.25, 0.63, 0.22, 0.36, 0.58, 0.39, 0.2, 0.4, 0.89, 0.92, 0.28, 0.38, 0.71, 0.988, 0.87, 0.12, 0.57, 0.966, 0.97, 0.9999, 0.72, 0.09, 0.15, 0.88, 0.994, 0.83, 0.998, 0.99999, 0.27, 0.45, 0.54, 0.68, 0.48, 0.75, 0.73, 0.79, 0.3, 0.08, 0.18, 0.55, 0.35, 0.51, 0.62, 0.968, 0.972, 0.974, 0.04, 0.06, 0.67, 0.33, 0.77, 0.96, 0.03, 0.32, 0.976, 0.0, 0.41, 0.44, 0.52, 0.42, 0.64, 0.82, 0.984, 0.978, 0.49, 0.61, 0.53, 0.999, 0.13, 0.8, 0.17, 0.78, 0.6, 0.69, 0.98, 0.982, 0.23, 0.964, 0.954, 0.91, 0.992, 0.24, 0.95, 0.47, 0.86, 0.34, 0.59, 0.26, 0.07, 0.996, 0.99, 0.81, 0.9, 0.29, 0.05, 0.7, 0.19, 0.46, 0.1, 0.958, 0.43, 0.74, 0.01, 0.14, 0.37, 0.02, 0.31, 0.986, 0.85, 0.956, 0.962, 0.56, 0.76, 0.952, 0.5]
    ptiles = []
    for i in tempo_ptiles:
        ptiles.append([i, numpy.percentile(npdata, i * 100)])
    ptiles.sort()
    return ptiles


def generate_csv_for_cdf_plot(csv_file, cdf_data, log=False):
    with open(csv_file, 'w+') as f:
        csvwriter = csv.writer(f)
        k = 1
        for i in range(len(cdf_data)):
            data = [cdf_data[i][1], cdf_data[i][0]]
            csvwriter.writerow(data)
