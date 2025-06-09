#!/usr/bin/env python3

import json
import os
from datetime import datetime

# Define file paths
storage_folder = os.path.join(os.path.dirname(__file__), "../storage")
alerts_file = os.path.join(storage_folder, "alerts_log.json")
config_file = os.path.join(os.path.dirname(__file__), "../config/config.json")

def load_config():
    """Loads configuration settings from config.json."""
    if not os.path.exists(config_file):
        return {"alerts_limit_count": 10}  # Default value

    with open(config_file, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {"alerts_limit_count": 10}  # Default if JSON is corrupted

def cleanup_old_alerts():
    """Keeps only the last 'alerts_limit_count' alerts in the JSON file, sorted by time."""
    config = load_config()
    alerts_limit = config.get("alerts_limit_count", 10)  # Default to 10 if missing

    if not os.path.exists(alerts_file):
        print("No alerts file found. Skipping cleanup.")
        return

    # Load existing alerts
    with open(alerts_file, "r") as file:
        try:
            alerts = json.load(file)
        except json.JSONDecodeError:
            print("JSON file is corrupted. Resetting file.")
            alerts = []

    # Sort alerts by timestamp (oldest first)
    def parse_timestamp(alert):
        """Convert timestamp string to datetime object for sorting."""
        try:
            return datetime.strptime(alert["timestamp"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return datetime.min  # Push invalid timestamps to the front

    alerts.sort(key=parse_timestamp)  # Sort by time

    # Keep only the last N alerts
    alerts = alerts[-alerts_limit:]

    # Save back to JSON
    with open(alerts_file, "w") as file:
        json.dump(alerts, file, indent=4)

    print(f"Cleanup completed: Only last {alerts_limit} alerts are kept, sorted by time.")

# Run the cleanup function
cleanup_old_alerts()