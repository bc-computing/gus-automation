import os

from csvs_to_plot import plot_csvs

csvs = ["replication-factor-gus-read.csv", "replication-factor-gus-write.csv",
        "replication-factor-giza-read.csv", "replication-factor-giza-write.csv"]

protocols = ["Gus-read", "Gus-write", "Giza-read", "Giza-write"]

plot_csvs(os.getcwd(), "layered", csvs, protocols)
