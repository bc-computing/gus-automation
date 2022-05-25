import glob
import os
import random


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

    print(regional_latency_counts)
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
