# Figure Plotting Library
## Table of Contents
- Dependencies
- Background
- Workflow
- Package Design
- How to Run

## Dependencies
### Code
- Python 3.10 (for running experiments automatically, calculating stats, plotting data)
- gnuplot
- matplotlibz


## Background
In order to understand the plotting code, one must understand what data is outputted by an experiment.

###  What is outputted from an experiment?
As they are running, each process (master, server, client) outputs information into two logs: a standard output log, and a standard error log. These files can provide useful information when experiments don't work as expected.

The client process in particular will produce some extra output. Detailed below are the outputs of interest.  

#### Latency
These are contained in files that start with `latFileRead` or `latFileWrite`. These files contain the latency of every client request that was sent during the experiment (the time in milliseconds between sending a request and getting a response from a server).

These latencies are organized in two ways: by operation type and server number. In order to analyze write commands and read commands separately, the latencies of read commands are stored in `latFileRead` and the latencies of the write commands are stored in `latFileWrite`. To plot data with the same amount of latencies from each server, the latencies are also seperated by server. For example, with 3 servers, there would be `latFileRead-0.txt`, `latFileRead-1.txt`, and `latFileRead-2.txt`.

#### Throughput
This is contained in a file called `lattput.txt`. Every couple of seconds while the experiment is running, the client will print a row of data into this file. One of the columns corresponds to the total throughput of the system (number of requests completed / time of experiment in seconds).

To get the average throughput of the system, we run `client_metrics.py` on the client folder, which will print out a dictionary of statistics. The exact statistics can be found by reading through the code.

## How to Run (for most plots)
1. Run `python3 plot_figs.py`
2. Results will be in the `plots` target directory.
