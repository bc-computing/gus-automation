# Figure Plotting Library

## Dependencies
### Code
- Python 3.8 (for running experiments automatically, calculating stats, plotting data)
- gnuplot  

## How to Run
1. Uncomment the relevant sections in the `main()` function of `plot_figs.py`. 
2. d
3. Run `python3.8 plot_figs.py`


## Background
In order to understand the plotting code, one must understand what data is outputted by an experiment.

###  What is outputted from an experiment?
As they are running, each process (master, server, client) outputs information into two logs: a standard output log, and a standard error log. These files can provide useful information when experiments don't work as expected.

The client process in particular will produce some extra output. Detailed below are the outputs of interest.  

#### Latency
These are contained in files that start with `latFileRead` or `latFileWrite`. These files contain the latency of every client request that was sent during the experiment (the time in milliseconds between sending a request and getting a response from a server).

These latencies are organized in two ways: by operation type and server number. In order to analyze write commands and read commands separately, the latencies of read commands are stored in `latFileRead` and the latencies of the write commands are stored in `latFileWrite`. To plot data with an even amount of latencies from each server, the latencies are also seperated by server. For example, with 3 servers, there would be `latFileRead-0.txt`, `latFileRead-1.txt`, and `latFileRead-2.txt`.

#### Throughput
This is contained in a file called `lattput.txt`. Every couple of seconds while the experiment is running, the client will print a row of data into this file. One of the columns corresponds to the total throughput of the system (number of requests completed / time of experiment in seconds).

To get the average throughput of the system, we run `client_metrics.py` on the client folder, which will print out a dictionary of statistics.

TODO: GET PICTURE OF CLIENT METRIC OUTPUT

## Workflow
Each set of figures vary in how data is collected and plotted. I will detail how each figure is plotted by their number in the Gus paper. These figures correspond to the data in the `latencies`, `throughput-latency`, `data-size-latencies`, and `write-ratio-throughput` folders. 

### Figure 6 - Tail Latency
Figure 6 graphs a cumulative distribution function of the latencies of gus, gryff, and epaxos with two independent variables: conflict percentage and operation type.

The workflow from experiment data to tail latency plots can be split into 3 steps: latency aggregation, percentile calculation, percentile plotting.

#### Latency Aggregation
Using the files inside the client log folder, we aggregate the latencies of a specific optype (for example, `latFileRead-0.txt`, `latFileRead-1.txt`, and `latFileRead-2.txt`) and store them in a python list.

When we aggregate the latencies, we "normalize" them to prevent the data from being skewed. By "normalize", we mean that if some servers were able to receive more client requests than other servers, we collect the same number of latencies from each server. For example, it is possible that server 0 only handled 12,000 client requests, while server 1 and 2 handled 13,000 client requests. In this case, we take 12,000 latencies from each server, randomly selecting a subset of the latencies. This way, the latencies of one server don't get more precedence than the other servers when we calculate percentiles.

Since figure 6 features the CDFs of both read and write latencies, we extract the normalized latencies of both reads and writes, for all 3 protocols, and all 3 conflict rates.

#### Percentile Calculation
Once the latencies are collected, we use numpy on the aggregated latencies, calculating 1 to 99 percentile latency (incrementing by 1 percentile). We then put these percentiles in a csv, with the second column containing the percentile and the first column containing the corresponding latency.

In addition to calculating 1 to 99 percentile latency, to really focus on the tail latency, we also calculate a log scaled cdf, with most percentile calculated being in between the 90th and 100th percentiles. Since the log scaled cdfs corresponded pretty nicely with the regular scaled cdfs, we chose not to show them in our paper.

Percentiles are calculated for all 3 protocols, all 3 conflict rates, and both optypes.

#### Percentile Plotting
With the data nicely formatted into csv files, we use gnuplot to plot the percentiles.

### Figure 7 - Tail Latency (n=5)
The workflow for figure 7 is the mostly the same as figure 6, except the conflict rate stays the same and latencies are aggregated from 5 servers instead of 3.

### Figure 8 - Throughput vs. p50/p99.9 Latency
Figure 8 requires data in a different format than the previous figures. In the interest of time, we manually collected and formatted the data for plotting. Automating this section will require some extra work. Below, I will detail the manual process.

To get the different throughput vs. latency points shown in the figure, we varied the number of clients that were communicating with the servers. Points with low latency/throughput corresponded with lower number of clients, points with high latency/throughput corresponded with a higher number of clients.

After running each experiment, we would run `client_metrics.py` on the resulting client folder. This would give us three stats of importance: p50 latency, p99.9 latency, and average throughput. We copied these stats into a single row of a csv file.

Afterwards, we plotted the csvs of each replication protocol using gnuplot. 

### Figure 9 - Write Ratio vs. Throughput
Figure 9 was also collected manually. We ran each replication protocol with the maximum clients it could handle without crashing, varied write percentage, and used `client_metrics.py` on the resulting client folders to give us average throughput. Afterwards, we plotted the csvs of each replication protocol using gnuplot.

### Figure 10 - Replication Factor vs. Latency (layered design)
Figure 10 was also collected manually. We ran experiments with the layered design version of gus (by switching branches) with different numbers of data servers, and used `client_metrics.py` on the resulting client folders to extract p99.99 read/write latency. Then we plotted with gnuplot.

### Figure 11 - Data Size vs Read Latency
Figure 11 was also collected manually, where we varied data size and used `client_metrics.py` to get p50 and p99 read latency with both giza and gus. Data was plotted with gnuplot.

## Package Design
For figures 6 and 7, `plot_figs.py`, `folders_to_norm_latencies.py`, `latencies_to_csv.py`, and `csvs_to_plot.py` were used. Figures 8-11 do not use `folders_to_norm_latencies.py` and `csvs_to_plot.py`. Below I will detail what each file does.

### plot_figs.py
This file acts as the main function for the plotting of the figures. The user inputs the folder locations of the necessary data, and uses the functions in the files listed below to transform the client folders into plots.

### folders_to_norm_latencies.py
The function `extract_norm_latencies()` will do the latency aggregation mentioned above.

### latencies_to_csv.py
Given a python list of latencies, the function `latencies_to_csv()` will calculate latency percentiles from 1 to 99 and put them in a csv, returning the path to the newly created csv file. It will also make a second csv with log scaled percentiles.

### csvs_to_plot.py
Each figure has a specific function in this file that will take the necessary csv files and plot the data using gnuplot like it appears in the paper.
___
TODO: one thing I realized after writing this doc is that the latency percentiles calculated via `client_metrics.py` did not normalize latencies like the code in `plot_figs.py`.
