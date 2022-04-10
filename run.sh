#!/bin/sh

python3.8 setup_network_delay_test.py config.json
python3.8 run_experiment_test.py config.json
