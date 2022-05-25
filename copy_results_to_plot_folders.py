from asyncio import protocols
import subprocess
import os


def copy_results(orig_parent_path):
    orig_parent_path += "\\"

    # change for each person
    
    figs  = []
    for x in os.scandir(orig_parent_path):
        if x.is_dir():
            figs.append((x.path)[x.path.index("fig"):])


    print(figs)
    

    for fig in figs:
        orig_path = orig_parent_path + fig + "\\"

        # Assumes there are resuls for gus, epaxos and gryff
        protocols = ["gus", "epaxos", "gryff"]

        for protocol in protocols:
            path = orig_path + protocol + "\\client\\*"

            # just the number
            stripped_fig  = fig[3:]

            plot_path = ".\\plotFigs\\latencies\\" + protocol + "\\" + stripped_fig + "\\"
            print(path)

            os.system("cp " + " -r " + path + " " + plot_path)


def get_parent_path():
    root = ".\\results\\"

    dirs  = []
    for x in os.scandir(root):
        if x.is_dir():
            dirs.append((x.path))


    print(dirs)

    dirs.sort(reverse=True)
    return dirs[0]



if __name__== "__main__":
    parent_path = get_parent_path()
    copy_results(parent_path)