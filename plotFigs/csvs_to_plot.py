import os
import subprocess
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from pathlib import Path
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib.ticker import FixedLocator, FuncFormatter

# Remove whitespace before "0" on x axis
# Compress y axis by 2x

# Look into thi
# https://github.com/matplotlib/matplotlib/blob/v3.5.3/lib/matplotlib/scale.py#L243-L257

# Defining lines and colors
colors = {"gryff":"green", "gus":"orange", "epaxos":"blue"}
linestyles = {"gryff":"dashdot", "gus":"solid", "epaxos":"dotted"}
labels = {"gryff":"Gryff", "gus":"Gus", "epaxos":"EPaxos"} # properly stylized

# New in development version with matplotlib
def cdf_csvs_to_plot(plot_target_directory, figure, csvs, is_for_reads, log=False):
    # Reformat function header to just pass csvs dictionary 
    # csvs = {"gus": gus_csv, "gryff":gryff_csv, "epaxos":epaxos_csv}
    print("csvs = " , csvs)

    # Each data object is a np array. 1st column is x data (latency), 2nd column is y data (percentile). label is the protocol
    # Creates data dictionary from csvs dictionary. Exclude anything beyond first two columns
    data = {protocol: np.genfromtxt(csv, delimiter=',', usecols=np.arange(0,2)) for protocol, csv in csvs.items()}
    
    fig, ax = plt.subplots()

    # sizing and margins
    fig.set_figheight(1.5)
    fig.set_figwidth(6)
    ax.margins(x=0.01)

    # d is data (singular)
    for protocol, d in data.items():
        print("d = ", d)
        ax.plot(d[:,0], d[:,1], color=colors[protocol], linestyle=linestyles[protocol], label=labels[protocol]) 
    
    # Setting scale for y axis
    if log == True:
        ax.set_yscale('log')
        ax.set_ylim(bottom=.01)
    # Adding labels
    ax.set_xlabel('Latency (ms)')

    if is_for_reads == True:
        ax.set_ylabel('Fraction of Reads')
    else:
        ax.set_ylabel('Fraction of Writes')
    
    ax.legend()

    fig.savefig(plot_target_directory / Path(figure + ".png") , bbox_inches="tight")


# # Used for figure 8 - new version of plotting with matplotlib
# # throughputs is a dictionary indexed via: thoughputs[protocol][wp]
# def tput_wp_plot(plot_target_directory, figure, throughputs):

#     fig, ax = plt.subplots()

#     # sizing and margins
#     fig.set_figheight(1.5)
#     fig.set_figwidth(6)
#     ax.margins(x=0.01)

#     print("throughputs = ", throughputs)

#     # d is data
#     for protocol, d  in throughputs.items():
#         d = np.sort(d) # sort the data before plotting
#         ax.plot(d[:,0], d[:,1], color=colors[protocol], linestyle=linestyles[protocol], label=labels[protocol]) 

#     ax.set_xlabel("Write Percentage")
#     ax.set_ylabel("Throughput (ops/s)")

#     ax.legend()

#     fig.savefig(plot_target_directory / Path(figure + ".png") , bbox_inches="tight")
