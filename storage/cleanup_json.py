#!/usr/bin/env python3

import json
import os
from datetime import datetime, timedelta

# Define JSON file path (relative to script)
storage_folder = os.path.join(os.path.dirname(__file__), "../storage")
json_file = os.path.join(storage_folder, "system_logs.json")
config_file = os.path.join(os.path.dirname(__file__), "../config.json")

# Load configuration
def load_config():
    """Loads the config settings from config.json or uses defaults."""
    default_config = {
        "history_limit_hours": 5,  # Default time-based deletion (older than X hours)
        "max_log_entries": 100  # Default max log entries
    }

    if not os.path.exists(config_file):
        print("config.json not found, using default cleanup settings.")
        return default_config

    try:
        with open(config_file, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("config.json is corrupted, using default cleanup settings.")
        return default_config

# Load settings
config = load_config()
TIME_LIMIT_HOURS = config["history_limit_hours"]
MAX_LOG_ENTRIES = config["max_log_entries"]

def cleanup_old_entries():
    """Removes entries older than the specified time limit and enforces max log size."""
    if not os.path.exists(json_file):
        print("No JSON file found. Skipping cleanup.")
        return

    # Read existing data
    with open(json_file, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print("JSON file is corrupted. Resetting file.")
            data = []

    # Get the current time
    now = datetime.now()
    time_limit = now - timedelta(hours=TIME_LIMIT_HOURS)

    # Filter out old entries
    filtered_data = [
        entry for entry in data
        if datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S") >= time_limit
        # strptime = Converts the string into a real datetime object
    ]

    # Enforce max log entries limit (FIFO - First In, First Out)
    if len(filtered_data) > MAX_LOG_ENTRIES:
        filtered_data = filtered_data[-MAX_LOG_ENTRIES:]  # Keep only the most recent entries

    # Save the cleaned data
    with open(json_file, "w") as file:
        json.dump(filtered_data, file, indent=4)

    print(f"Cleanup completed: {len(data) - len(filtered_data)} old entries removed.")
    print(f"Log size after cleanup: {len(filtered_data)} entries.")

# Run the cleanup function
cleanup_old_entries()