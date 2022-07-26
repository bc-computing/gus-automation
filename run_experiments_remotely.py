import os
import sys


def usage():
    print("Usage: python3 run_experiments_remotely <USER@EXPERIMENT_IP_OR_ADDRESS> <fig#> <fig#> ...")

def run_remote_command(ssh, command):
    os.system(ssh + " '" + command + "'")

# Runs root command from /root/go/src/gus-automation
def run_remote_root_command(ssh, command):
    run_remote_command(ssh, "sudo bash -c 'cd /root/go/src/gus-automation && " + command + "'")

def main():
    ssh = "ssh -A " + sys.argv[1]
    figs = sys.argv[2:]

    figs_string = ' '.join(figs)
    command = "sudo python3 run_experiments.py " + figs_string # maybe add in absolute path: /root/go/src/gus-automation
    run_remote_root_command(ssh, command)




if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
    else:
        main()