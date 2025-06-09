#!/usr/bin/env python3

import json
import os
from datetime import datetime, timedelta
from send_alert import send_email_alert  # Import email function

# Define paths
storage_folder = os.path.join(os.path.dirname(__file__), "../storage")
json_file = os.path.join(storage_folder, "system_logs.json")
config_file = os.path.join(os.path.dirname(__file__), "../config/config.json")

# Load crisis thresholds from config.json
def load_config():
    """Load crisis thresholds from config.json, use defaults if missing."""
    default_config = {
        "cpu_threshold": 90,
        "ram_threshold": 85,
        "disk_threshold": 90,
        "process_threshold": 500,
        "time_limit_minutes": 5
    }

    if not os.path.exists(config_file):
        print("config.json not found, using default thresholds.")
        return default_config

    try:
        with open(config_file, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("config.json is corrupted, using default thresholds.")
        return default_config

# Load configuration
config = load_config()

def detect_crisis():
    """Scans logs for a crisis situation and triggers an alert if needed."""
    if not os.path.exists(json_file):
        print("No logs found. Skipping crisis check.")
        return

    # Read logs
    with open(json_file, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print("JSON file is corrupted. Skipping crisis check.")
            return

    # Get recent logs (last X minutes, from config)
    now = datetime.now()
    time_limit = now - timedelta(minutes=config["time_limit_minutes"])
    
    for entry in data:
        timestamp = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
        if timestamp >= time_limit:
            server = entry["server_id"]
            timestamp_str = entry["timestamp"]
            metric = entry["metric_type"]
            value = entry["value"]
            
            # Convert value to float if necessary
            try:
                if isinstance(value, str):
                    value = float(value.replace("%", ""))
                else:
                    value = float(value)
            except ValueError:
                continue  # Skip non-numeric values

            # Check for crisis conditions (based on config thresholds)
            if "CPU" in metric and value > config["cpu_threshold"]:
                send_email_alert(server, metric, value, timestamp_str)
            if "RAM" in metric and value > config["ram_threshold"]:
                send_email_alert(server, metric, value, timestamp_str)
            if "Disk" in metric and value > config["disk_threshold"]:
                send_email_alert(server, metric, value, timestamp_str)
            if "Processes" in metric and value > config["process_threshold"]:
                send_email_alert(server, metric, value, timestamp_str)

# Run crisis detection
detect_crisis()