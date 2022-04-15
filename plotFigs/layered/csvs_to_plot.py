import os
import subprocess

def plot_csvs(plot_target_directory, figure, csvs, protocols):
    plot_script_file = os.path.join(plot_target_directory, '%s.gpi' % figure)
    generate_cdf_gnuplot_script(plot_script_file, plot_target_directory, csvs, protocols)
    subprocess.call(['gnuplot', plot_script_file])

def generate_cdf_gnuplot_script(plot_script_file, plot_target_directory, csvs, protocols):
    with open(plot_script_file, 'w+') as f:
        f.write("set datafile separator ','\n")
        f.write("set terminal pngcairo size 2100,500 enhanced font 'Helvetica,36'\n")

        f.write("set key horizontal tmargin\n")
        f.write("set xlabel 'Replication Factor'\n")
        f.write("set ylabel 'Latency (ms)'\n")
        f.write("set ytics 200\n")

        f.write('set output \'%s/%s\'\n' % (".", os.path.splitext(os.path.basename(plot_script_file))[0] + '.png'))

        f.write('set style line 1 linecolor "orange" pointtype 7 linewidth 6\n')
        f.write('set style line 2 linecolor "orange-red" pointtype 11 linewidth 6\n')
        f.write('set style line 3 linecolor "blue" pointtype 4 linewidth 6 dashtype 2\n')
        f.write('set style line 4 linecolor "slateblue1" pointtype 13 linewidth 6 dashtype 2\n')

        f.write('plot ')
        for i in range(len(csvs)):
            f.write("'%s' using 1:2 title '%s' with linespoints linestyle %d" % (csvs[i], protocols[i], i + 1))
            if i != len(csvs) - 1:
                f.write(', \\\n')