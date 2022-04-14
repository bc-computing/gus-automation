import os
import subprocess

# for figures 6 and 7
def plot_csvs(plot_target_directory, figure, csvs, protocols):
    plot_script_file = os.path.join(plot_target_directory, '%s.gpi' % figure)
    generate_cdf_gnuplot_script(plot_script_file, plot_target_directory, csvs, protocols)
    subprocess.call(['gnuplot', plot_script_file])

def generate_cdf_gnuplot_script(plot_script_file, plot_target_directory, csvs, protocols):
    with open(plot_script_file, 'w+') as f:
        f.write("set datafile separator ','\n")
        f.write("set terminal pngcairo size 1500,500 enhanced font 'Helvetica,36'\n")

        f.write("set key outside top\n")
        f.write("set xlabel 'Latency (ms)'\n")
        f.write("set ylabel 'Percentiles'\n")

        f.write('set output \'%s/%s\'\n' % (".", os.path.splitext(os.path.basename(plot_script_file))[0] + '.png'))

        # f.write('set style line 1 linetype 1 linecolor "web-green" linewidth 6 dashtype 4\n')
        # f.write('set style line 2 linetype 1 linecolor "orange" linewidth 6 dashtype 1\n')
        # f.write('set style line 3 linetype 1 linecolor "blue" linewidth 6 dashtype 3\n')

        f.write('plot ')
        for i in range(len(csvs)):
            f.write("'%s' using 1:(-log10(1-$2)):yticlabels(3) title '%s' with linespoints" % (csvs[i], protocols[i]))
            if i != len(csvs) - 1:
                f.write(', \\\n')