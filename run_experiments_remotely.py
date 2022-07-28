import subprocess
import sys

# Remote commands are not running properly

def usage():
    print("Usage: python3 run_experiments_remotely <USER@EXPERIMENT_IP_OR_ADDRESS> <fig#> <fig#> ...")

def run_remote_command(ssh, command):

    with subprocess.Popen(ssh + " '" + command + "'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        output, error = process.communicate()
        print(output.decode("utf-8"))
        print(error.decode("utf-8"))
        process.wait()
    print("command = " + command)
    
 

# Runs root command from /root/go/src/gus-automation
def run_remote_root_command(ssh, command):
    run_remote_command(ssh, "sudo bash -c \" cd /root/go/src/gus-automation && " + command + "\"")

def main():
    #subprocess.Popen("ssh -A dumasca@ms1110.utah.cloudlab.us \"sudo bash -c 'cd /root/ && touch yo.txt' \"", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    ssh = "ssh -A " + sys.argv[1]
    print("ssh is " + ssh)
    figs = sys.argv[2:]

    figs_string = ' '.join(figs)
    command = "sudo python3 run_experiments.py " + figs_string # maybe add in absolute path: /root/go/src/gus-automation
    #command = "python3 test.py"
    run_remote_root_command(ssh, command)
    run_remote_root_command(ssh, "sudo python3 run_experiment_test.py configs/fig7.json")
    print("done running")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
    else:
        main()