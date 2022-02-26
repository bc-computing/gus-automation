import subprocess


def copy_local_directory_to_remote(local_path, remote_url, remote_path, exclude_paths=[]):
    # Note: a trailing slash on the source directory will copy the contents of the directory, not the directory itself.
    args = ["rsync", "-r", "-e", "ssh", "%s/" % local_path, "%s:%s" % (remote_url, remote_path)]
    subprocess.call(args)

def copy_remote_directory_to_local(local_path, remote_url, remote_path, exclude_paths=[]):
    args = ["rsync", "-r", "-e", "ssh", "%s:%s/" % (remote_url, remote_path), local_path]
    subprocess.call(args)


def get_machine_url(config, server_name):
    return "%s@%s" % (config['cloudlab_user'],
                      (config['host_format_str'] % (server_name, config['experiment_name'], config['project_name'])))


def tcsh_redirect_output_to_files(command, stdout_file, stderr_file):
    return '(%s > %s) >& %s' % (command, stdout_file, stderr_file)


def run_remote_command_sync(command, remote_url):
    print("contacting %s with command %s" % (remote_url, command))
    return subprocess.run(ssh_args(command, remote_url),
                          stdout=subprocess.PIPE, universal_newlines=True).stdout


def run_remote_command_async(command, remote_url):
    print("contacting %s with command %s asynchronously" % (remote_url, command))
    return subprocess.Popen(ssh_args(command, remote_url))


def ssh_args(command, remote_url):
    return ["ssh", '-o', 'StrictHostKeyChecking=no',  # can connect with machines that are not in the known host list
            '-o', 'ControlMaster=auto',  # multiplex ssh connections with a single tcp connection
            '-o', 'ControlPersist=2m',  # after the first connection is closed, use tcp connection for up to 2 minutes
            '-o', 'ControlPath=~/.ssh/cm-%r@%h:%p',  # location of the control socket
            remote_url, command]