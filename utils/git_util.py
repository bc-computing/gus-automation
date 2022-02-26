import subprocess


def get_current_branch(src_directory):
    return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=src_directory).rstrip()


def checkout_branch_hard_reset(src_directory, branch):
    hard_reset(src_directory)
    checkout_branch(src_directory, branch)

def hard_reset(src_directory):
    subprocess.call(["git", "reset", "--hard"], cwd=src_directory)

def checkout_branch(src_directory, branch):
    subprocess.call(["git", "checkout", branch], cwd=src_directory)
