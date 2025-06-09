#!/usr/bin/env python3

import os

def fetch_serverb_logs():
    remote_user = "serverb"
    remote_ip = "192.168.64.12"
    remote_path = "/home/serverb/AMS_Project/storage/system_logs.json"
    local_path = os.path.expanduser("~/AMS_Project/storage/remote/serverb_logs.json")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    # Use SCP to copy the file from Server B to the local machine
    result = os.system(f"scp {remote_user}@{remote_ip}:{remote_path} {local_path}")
    if result != 0:
        print("Error: SCP failed, unable to fetch logs from Server B.")
        return

    # After fetching, open the copied file and read the content
    try:
        with open(local_path, "r") as file:
            file_content = file.read()
    except Exception as e:
        print(f"Error: Failed to read the copied file - {e}")
        return

    # Define the new path in your local storage/remote folder where you want to copy the content
    final_local_path = os.path.join(os.path.dirname(__file__), "../storage/remote/system_logs.json")

    # Write the content into the new file
    try:
        with open(final_local_path, "w") as output_file:
            output_file.write(file_content)
        print(f"Content from serverb_logs.json has been copied to {final_local_path}")
    except Exception as e:
        print(f"Error: Failed to write to the new file - {e}")

# Call the function
fetch_serverb_logs()