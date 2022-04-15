#!/usr/local/bin/python3

# Copyright (c) 2020 Stanford University
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR(S) DISCLAIM ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL AUTHORS BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
This file computes key metrics from Paxos client logfiles. The logfile format is
specified in src/client/client.go.
"""
import glob
import json
import os

import numpy as np
from os import path
import statistics

import sys


def get_metrics(dirname):
    """
    Computes key metrics about an experiment from the client-side logfiles, and
    returns them as a dictionary. 'dirname' specifies the directory in which the
    client-side logfiles are stored.
    """
    with open(path.join(dirname, 'lattput.txt')) as f:
        tputs = []
        for l in f:
            l = l.split(' ')
            tputs.append(float(l[2]))


    read_log_files = glob.glob(os.path.join(dirname, "latencyRead*"))
    reads = []
    for read_log_file in read_log_files:
        with open(read_log_file) as f:
            for l in f:
                l = l.split(' ')
                reads.append(float(l[1]))

    write_log_files = glob.glob(os.path.join(dirname, "latencyWrite*"))
    writes = []
    for write_log_file in write_log_files:
        with open(write_log_file) as f:
            for l in f:
                l = l.split(' ')
                writes.append(float(l[1]))

    return {
        # 'mean_Read': statistics.mean(reads),
        # 'p50_Read': np.percentile(reads, 50),
        # 'p90_Read': np.percentile(reads, 90),
        # 'p95_Read': np.percentile(reads, 95),
        # 'p99_Read': np.percentile(reads, 99),
        # 'p999_Read': np.percentile(reads, 99.9),
        'p9999_Read': np.percentile(reads, 99.99),
        # 'mean_Write': statistics.mean(writes),
        # 'p50_Write': np.percentile(writes, 50),
        # 'p90_Write': np.percentile(writes, 90),
        # 'p95_Write': np.percentile(writes, 95),
        # 'p99_Write': np.percentile(writes, 99),
        # 'p999_Write': np.percentile(writes, 99.9),
        'p9999_Write': np.percentile(writes, 99.99),
        # 'avg_tput': statistics.mean(tputs),
    }

if __name__ == '__main__':
    """
    Computes client metrics from the root epaxos directory, which is where the
    files are stored on the remote client machines. Logs the metrics to stdout
    in json format.
    """

    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python3 %s <path_to_folder>\n' % sys.argv[0])
        sys.exit(1)

    print(json.dumps(get_metrics(sys.argv[1])))