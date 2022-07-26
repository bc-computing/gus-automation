import os
import sys


def usage():
    print("Usage: python3 run_experiments_remotely <USER@EXPERIMENT_IP_OR_ADDRESS> <fig#> <fig#> ...")

def run_remote_command(ssh, command):
    os.system(ssh + " '" + command + "'")

def main():
    ssh = "ssh -A " + sys.argv[1]
    figs = sys.argv[2:]

    figs_string = ' '.join(figs)
    command = "sudo python3 /root/go/src/gus-automation/run_experiments.py " + figs_string
    run_remote_command(ssh, command)




if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
    else:
        main()