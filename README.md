# Gus Experiment Automation
This repo consists of python code that will autonomously run the replication protocol experiments cited in our paper and plot them. See `config_instruction.md` for information on available configs. 

## Dependencies
### Code
- Go 1.15 (for replication protocol code)
- Python 3.8 (for running experiments automatically, calculating stats, plotting data)
- Redis 6.2.2 (for a specific experiment configuration)
### Repositories
- The gus repository
- The gryff repository 
- Note: Both repositories are derived from the epaxos repository, but have different communication between clients and servers, so it is easier to have two seperate repos.

All of the dependencies mentioned above are preinstalled in the control machine in `/root/go/src` in this [cloudlab profile](https://www.cloudlab.us/p/fff5448808f3ecb656874213ea663bd448544a7e).

## How to Run
### Single Experiment
1. Run `python3.8 setup_network_delay_test.py config.json` to create artificial delay between servers in order to simulate a WAN. This only needs to be run once.
2. Modify `config.json` to choose the settings for the experiment that will be run.
3. Run `python3.8 run_experiment_test.py config.json` to run the experiment. 
### Multiple Experiments
TODO

## Workflow
### Single Experiment
The execution of an experiment can be seperated into two phases: setup and execution. Detailed below is what our code is doing.

#### Setup
In the control machine,
1. Switch to the correct branch depending on if n=3 or n=5. Stash changes if they were made when switching.
   1. There are some pretty important differences between running gus with 3 servers and 5 servers. Thus, we decided to make two seperate brances for n=3 and n=5. 
   2. The difference between running gryff with 3 servers and 5 servers isn't as much, but for simplicity, we decided to have two seperate branches for gryff as well.
2. Compile the master, server, client binaries.
   1. Both the gryff and gus repository binaries are compiled and stored in seperate folders.
3. Create a timestamped result directory.
   1. The directory is named after the current time to distnguish it from the result folders of other experiments.
   2. This directory will contain the output from each server and client machine.

In each server and client machine,
4. Create a result folder (with the same timestamp) to store its own results.
5. Create a folder to store binaries.
6. Download the binaries from the control machine.

#### Execution
1. Kill any processes on the client and server machines that are named `master`, `server`, or `client` for safety.
2. Execute master, server, client binaries on their respective machines.
3. Once the client process finishes, kill all master and server processes.
4. Download the logs of each master, client, and server process into the control machine.

Note: I am deferring the automatic calculation of stats and plotting for later. 

### Multiple Experiments
TODO

## Package Design
There are 3 primary python files: `setup_network_delay.py`, `setup_nodes.py`, `run_experiment.py`. These contain functions that are the core of the automation code. 

These primary python files call helper functions contained in the utils folder. 
- `remote_util.py` contains functions for interacting with the client and server machines via ssh and scp. 
- `command_util.py` contains functions that will return commands for executing binaries.
- `git_util.py` contains functions for interacting with the gus-epaxos and gryff repositories.

The auxiliary test files `setup_network_delay_test.py`, `setup_nodes_test.py`, `run_experiment_test.py` invoke the functions in their respective files, `run_experiment_test.py` also calls some functions from `setup_node.py`.
