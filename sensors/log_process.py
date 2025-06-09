#!/usr/bin/env python3
import psutil
from log_data import log_data

num_processes = len(psutil.pids())
# psutil.pids() = list of all currently running process IDs (PIDs) on the machine

log_data("Processes", num_processes)