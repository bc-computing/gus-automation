import subprocess


def get_current_branch(src_directory):
    return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=src_directory,
                                   universal_newlines=True).rstrip()

def stash(src_directory):
    subprocess.call(["git", "stash"], cwd=src_directory)

def hard_reset(src_directory):
    subprocess.call(["git", "reset", "--hard"], cwd=src_directory)

def checkout_branch(src_directory, branch):
    subprocess.call(["git", "checkout", branch], cwd=src_directory)
