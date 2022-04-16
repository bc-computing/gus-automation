import os

from csvs_to_plot import plot_csvs

csvs = ["replication-factor-gus-read.csv", "replication-factor-gus-write.csv",
        "replication-factor-giza-read.csv", "replication-factor-giza-write.csv"]

protocols = ["Gus-read", "Gus-write", "Giza-read", "Giza-write"]

# plot_csvs(os.getcwd(), "layered", csvs, protocols)
# interleaved
plot_csvs(os.getcwd(), "layered", list(sum(zip(csvs[0:2], csvs[2:4]), ())), list(sum(zip(protocols[0:2], protocols[2:4]), ())))