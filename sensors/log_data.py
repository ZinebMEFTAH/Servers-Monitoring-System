#!/usr/bin/env python3

import json
# read and write logs in JSON format
import os
# work with file paths
from datetime import datetime
# to generate a timestamp

# Define JSON file path (absolute path based on script location)
base_dir = os.path.abspath(os.path.dirname(__file__))
# the directory where the current script is
storage_folder = os.path.join(base_dir, "../storage")
# go storage/ folder one level above this script
json_file = os.path.join(storage_folder, "system_logs.json")
# Final path to where the system logs are saved

# Ensure the storage folder exists
os.makedirs(storage_folder, exist_ok=True)

# Identifier for the machine (update if needed)
SERVER_ID = "local_machine"

def log_data(metric_type, value):
    """Logs system metrics into a JSON file with a fixed size."""
    entry = {
        "server_id": SERVER_ID,
        "metric_type": metric_type,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "value": value
    }

    # Load existing logs or initialize new list
    try:
        if os.path.exists(json_file):
            with open(json_file, "r") as file:
                data = json.load(file)
        else:
            data = []
    except json.JSONDecodeError:
        data = []

    # Append the new entry
    data.append(entry)

    # Save back to file
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)
    # indent=4 makes the JSON human-readable.

    print(f"Logged {metric_type}: {value} (Total Entries: {len(data)})")