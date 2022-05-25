import json
import os

from folder_to_norm_latencies import extract_norm_latencies
from extract_latencies import extract_latencies
from latencies_to_csv import tempo_json_to_csv, gus_latencies_to_csv
from csvs_to_plot import plot_csvs

gus_folders = ["client gus-5", "client gus-7", "client gus-9"]
gus_read_latencies = []
gus_write_latencies = []
gus_read_csvs = []
gus_write_csvs = []

tempo_jsons = ["exp_data_tempo52.json", "exp_data_tempo72.json", "exp_data_tempo92.json"]
tempo_csvs = []

# GUS
# Extract latencies
for gus_folder in gus_folders:
    gus_read_latencies.append(extract_norm_latencies(gus_folder, is_for_reads=True))
    gus_write_latencies.append(extract_norm_latencies(gus_folder, is_for_reads=False))

# Convert latencies to csv
for i in range(len(gus_read_latencies)):
    gus_read_csvs.append(gus_latencies_to_csv(gus_read_latencies[i], "gus-read-%d" % i))
    gus_write_csvs.append(gus_latencies_to_csv(gus_write_latencies[i], "gus-write-%d" % i))

# TEMPO
for i in range(len(tempo_jsons)):
    tempo_csvs.append(tempo_json_to_csv(tempo_jsons[i], "tempo-%d" % i))

csvs = gus_read_csvs + gus_write_csvs + tempo_csvs
protocols = ["Gus-read-5", "Gus-read-7", "Gus-read-9",
             "Gus-write-5", "Gus-write-7", "Gus-write-9",
             "Tempo-5", "Tempo-7", "Tempo-9"]


# interleave gus and tempo so it looks nice on the graph
plot_csvs(os.getcwd(), "scale-gus-read", list(sum(zip(gus_read_csvs, tempo_csvs), ())), list(sum(zip(protocols[0:3], protocols[6:9]), ())))
plot_csvs(os.getcwd(), "scale-gus-write", list(sum(zip(gus_write_csvs, tempo_csvs), ())), list(sum(zip(protocols[3:6], protocols[6:9]), ())))

