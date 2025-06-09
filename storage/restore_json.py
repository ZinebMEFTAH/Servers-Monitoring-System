#!/usr/bin/env python3

import os
import shutil

# Paths
storage_folder = os.path.join(os.path.dirname(__file__), "../storage")
backup_folder = os.path.join(os.path.dirname(__file__), "../backups")
json_file = os.path.join(storage_folder, "system_logs.json")

def restore_backup():
    """Restores a backup file to system_logs.json"""
    backups = sorted(os.listdir(backup_folder), reverse=True)  # Get all backups (latest first)

    if not backups:
        print("No backups available.")
        return

    # Show available backups
    print("\nAvailable Backups:")
    for i, backup in enumerate(backups):
        print(f"{i + 1}. {backup}")

    # Ask the user which backup to restore
    choice = input("\nEnter the backup number to restore (or 'q' to quit): ").strip()

    if choice.lower() == 'q':
        print("Restore canceled.")
        return

    try:
        choice = int(choice) - 1
        if choice < 0 or choice >= len(backups):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    # Restore selected backup
    selected_backup = os.path.join(backup_folder, backups[choice])
    shutil.copy(selected_backup, json_file)
    print(f"Restored {selected_backup} to {json_file}")

# Run the restore function
restore_backup()