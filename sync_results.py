import os

def sync_results():

    cmd = "rsync -a dumasca@control.test.hyflowtm-pg0.utah.cloudlab.us:/results/ results/"
    os.system(cmd)

if __name__ == "__main__":
    
    sync_results()
