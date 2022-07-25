import os

def sync_results():
    os.system("mkdir -p results")

    cmd = "rsync -a dumasca@control.test.hyflowtm-pg0.utah.cloudlab.us:results/ results/"
    os.system(cmd)

if __name__ == "__main__":
    sync_results()
