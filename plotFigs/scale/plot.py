import json
import os

from extract_latencies import extract_latencies
from latencies_to_csv import tempo_json_to_csv, gus_latencies_to_csv
from csvs_to_plot import plot_csvs

gus_folders = ["client gus-3", "client gus-7", "client gus-9"]
gus_latencies = []
gus_csvs = []

tempo_jsons = ["exp_data_tempo31.json", "exp_data_tempo72.json", "exp_data_tempo92.json"]
tempo_csvs = []

# GUS
# Extract latencies
for gus_folder in gus_folders:
    gus_latencies.append(extract_latencies(gus_folder))

# Convert latencies to csv
for i in range(len(gus_latencies)):
    gus_csvs.append(gus_latencies_to_csv(gus_latencies[i], "gus-%d" % i))

# TEMPO
for i in range(len(tempo_jsons)):
    tempo_csvs.append(tempo_json_to_csv(tempo_jsons[i], "tempo-%d" % i))

csvs = gus_csvs + tempo_csvs
protocols = ["gus-3", "gus-7", "gus-9", "tempo-3", "tempo-7", "tempo-9"]
plot_csvs(os.getcwd(), "scale", csvs, protocols)
