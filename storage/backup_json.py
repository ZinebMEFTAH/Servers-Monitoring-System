#!/usr/bin/env python3

import os
import shutil
from datetime import datetime

# Paths
storage_folder = os.path.join(os.path.dirname(__file__), "../storage")
backup_folder = os.path.join(os.path.dirname(__file__), "../backups")
json_file = os.path.join(storage_folder, "system_logs.json")

# Ensure backup folder exists
if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)

MAX_BACKUPS = 10  # Keep only the last 10 backups

def backup_logs():
    """Creates a backup of the JSON file with a timestamp."""
    if not os.path.exists(json_file):
        print("No JSON file found. Skipping backup.")
        return

    # Generate backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_folder, f"backup_{timestamp}.json")

    # Copy the JSON file to the backup folder
    shutil.copy(json_file, backup_file)
    print(f"Backup created: {backup_file}")

    # Maintain only the last MAX_BACKUPS files (FIFO)
    backups = sorted(os.listdir(backup_folder))  # Get all backups
    if len(backups) > MAX_BACKUPS:
        oldest_backup = os.path.join(backup_folder, backups[0])  # Oldest file
        os.remove(oldest_backup)  # Delete oldest backup
        print(f"Deleted old backup: {oldest_backup}")

# Run the backup function
backup_logs()