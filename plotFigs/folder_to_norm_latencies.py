import glob
import os
import random


def extract_norm_latencies(folder, is_for_reads):
    if is_for_reads:
        log_files = glob.glob(os.path.join(folder, "latFileRead*"))
    else:
        log_files = glob.glob(os.path.join(folder, "latFileWrite*"))

    norm_latencies = []
    regional_latencies = []
    regional_latency_counts = []

    # Convert regional latencies into a 2D list and count how many operations were recorded in each region.
    for log_file in log_files:
        with open(log_file) as f:
            ops = f.readlines()
            regional_latencies.append(ops)
            regional_latency_counts.append(len(ops))

    print(regional_latency_counts)
    latencies_to_take = min(regional_latency_counts)

    # Sample an equal amount of latencies from each region to "normalize" the data. Only extract the latency field.
    for latencies_in_region in regional_latencies:
        sample = random.sample(latencies_in_region, latencies_to_take)
        latencies_to_add = [float(op.split(" ")[1]) for op in sample]
        norm_latencies += latencies_to_add

    return norm_latencies
