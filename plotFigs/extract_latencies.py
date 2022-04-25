import glob
import os
import random


def extract_latencies(folder, is_for_reads):
    if is_for_reads:
        log_files = glob.glob(os.path.join(folder, "latFileRead*"))
    else:
        log_files = glob.glob(os.path.join(folder, "latFileWrite*"))

    latencies = []
    # Convert regional latencies into a 2D list and count how many operations were recorded in each region.
    for log_file in log_files:
        with open(log_file) as f:
            ops = f.readlines()
            latencies += [float(op.split(" ")[1]) for op in ops]

    print(len(latencies))
    return latencies
