import os
import subprocess

# for figures 6 and 7
def cdf_csvs_to_plot(plot_target_directory, figure, gryff_csv, gus_csv, epaxos_csv, is_for_reads, log=False):

    plot_script_file = os.path.join(plot_target_directory, '%s.gpi' % figure)

    csvs = (gryff_csv, gus_csv, epaxos_csv)
    protocols = ["Gryff", "Gus", "EPaxos"]  # should match with csvs passed in
    generate_cdf_gnuplot_script(plot_script_file, plot_target_directory, csvs, protocols, figure, is_for_reads=is_for_reads, log=log)
    subprocess.call(['gnuplot', plot_script_file])


def generate_cdf_gnuplot_script(plot_script_file, plot_target_directory, csvs, protocols, figure, is_for_reads, log=False):
    with open(plot_script_file, 'w+') as f:
        f.write("set datafile separator ','\n")
        f.write("set terminal pngcairo size 1500,500 enhanced font 'Helvetica,36'\n")

        if '7' in figure:
            if log:
                f.write("set key at graph 0.85, 0.725\n")
            else:
                f.write("set key at graph 0.9, 0.725\n")

        else:
            f.write("set key bottom right\n")


        f.write("set xlabel 'Latency (ms)'\n")
        if is_for_reads:
            f.write("set ylabel 'Fraction of Reads'\n")
        else:
            f.write("set ylabel 'Fraction of Writes'\n")

        f.write("set ytics .2\n")

        if '6' in figure:
            f.write("set xrange [0:300]\n")

        f.write('set output \'%s/%s\'\n' % (plot_target_directory, os.path.splitext(os.path.basename(plot_script_file))[0] + '.png'))

        f.write('set style line 1 linetype 1 linecolor "web-green" linewidth 6 dashtype 4\n')
        f.write('set style line 2 linetype 1 linecolor "orange" linewidth 6 dashtype 1\n')
        f.write('set style line 3 linetype 1 linecolor "blue" linewidth 6 dashtype 3\n')

        f.write('plot ')
        for i in range(len(csvs)):
            if log:
                f.write("'%s' using 1:(-log10(1-$2)):yticlabels(3) title '%s' ls %d with lines" % (csvs[i], protocols[i], i + 1))
            else:
                f.write("'%s' title '%s' ls %d with lines" % (csvs[i], protocols[i], i + 1))
            if i != len(csvs) - 1:
                f.write(', \\\n')

# for figure 9
def write_ratio_throughput_csvs_to_plot(plot_target_directory, gryff_csv, gus_csv, epaxos_csv):
    plot_script_file = os.path.join(plot_target_directory, 'write_ratio-throughput.gpi')

    csvs = (gryff_csv, gus_csv, epaxos_csv)
    protocols = ["Gryff", "Gus", "EPaxos"]  # should match with csvs passed in
    generate_write_ratio_throughput_gnuplot_script(plot_script_file, plot_target_directory, csvs, protocols)
    subprocess.call(['gnuplot', plot_script_file])

def generate_write_ratio_throughput_gnuplot_script(plot_script_file, plot_target_directory, csvs, protocols):
    with open(plot_script_file, 'w+') as f:
        # f.write("set datafile separator ','\n")
        f.write("set terminal pngcairo size 575,250 enhanced font 'Helvetica,18'\n")

        f.write("set key center tmargin\n")
        f.write("set key horizontal\n")

        f.write("set xlabel 'Write Ratio'\n")
        f.write("set ylabel 'Throughput (ops/s)'\n")

        f.write("set xtics .2\n")
        f.write("set ytics 1000\n")

        f.write('set output \'%s/%s\'\n' % (plot_target_directory, os.path.splitext(os.path.basename(plot_script_file))[0] + '.png'))

        f.write('set style line 1 linecolor "web-green" linewidth 6 pointtype 26 pointsize 1 dashtype 4\n')
        f.write('set style line 2 linecolor "orange" linewidth 6 pointtype 20 pointsize 1 dashtype 1\n')
        f.write('set style line 3 linecolor "blue" linewidth 6 pointtype 22 pointsize 1 dashtype 3\n')

        f.write('plot ')
        for i in range(len(csvs)):
            f.write("'%s' title '%s' with linespoints linestyle %d" % (csvs[i], protocols[i], i + 1))
            if i != len(csvs) - 1:
                f.write(', \\\n')

# for figure 11
def data_size_latencies_csvs_to_plot(plot_target_directory, gus_csv, giza_csv):
    plot_script_file = os.path.join(plot_target_directory, 'data_size-latencies.gpi')

    csvs = (gus_csv, giza_csv)
    protocols = ["Gus", "Giza"]  # should match with csvs passed in

    generate_data_size_latencies_gnuplot_script(plot_script_file, plot_target_directory, csvs, protocols)
    subprocess.call(['gnuplot', plot_script_file])

def generate_data_size_latencies_gnuplot_script(plot_script_file, plot_target_directory, csvs, protocols):
    with open(plot_script_file, 'w+') as f:
        f.write("set datafile separator ','\n")
        f.write("set terminal pngcairo size 300,200 enhanced font 'Helvetica,12'\n")

        f.write("set key center tmargin\n")
        f.write("set key horizontal\n")

        f.write("set xlabel 'Data Size (MB)'\n")
        f.write("set ylabel 'Latency (ms)'\n")

        f.write("set ytics 50\n")
        f.write("set logscale x 10\n")

        f.write('set output \'%s/%s\'\n' % (plot_target_directory, os.path.splitext(os.path.basename(plot_script_file))[0] + '.png'))

        f.write('set style line 1 linecolor "orange" linewidth 6 pointtype 20 pointsize 1 dashtype 1\n')
        f.write('set style line 2 linecolor "orange" linewidth 6 pointtype 20 pointsize 1 dashtype 3\n')
        f.write('set style line 3 linecolor "dark-yellow" linewidth 6 pointtype 13 pointsize 1 dashtype 1\n')
        f.write('set style line 4 linecolor "dark-yellow" linewidth 6 pointtype 13 pointsize 1 dashtype 3\n')

        f.write('plot ')
        latency_columns = [2, 3]
        latency_to_percentile = {2: "p50", 3: "p99"}
        for i in range(len(csvs)):
            for j in range(len(latency_columns)):
                f.write("'%s' using 1:%d title '%s-%s' with linespoints linestyle %d" % (csvs[i], latency_columns[j], protocols[i], latency_to_percentile[latency_columns[j]], i * len(latency_columns) + j + 1))
                f.write(', \\\n')