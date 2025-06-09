#!/usr/bin/env python3
import psutil
from log_data import log_data

ram_usage = psutil.virtual_memory().percent
# virtual_memory() = tuple with a lot of info

log_data("RAM", ram_usage)