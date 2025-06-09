#!/usr/bin/env python3

import json
import os
import pygal
from datetime import datetime

# Base paths
base_dir = os.path.abspath(os.path.dirname(__file__))
storage_folder = os.path.join(base_dir, "../storage")
local_file = os.path.join(storage_folder, "system_logs.json")
serverb_file = os.path.join(os.path.dirname(__file__), "../storage/remote/system_logs.json")
output_folder = os.path.join(base_dir, "../graphs")

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

def load_logs(file_path):
    """Load logs from a single file."""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Corrupted: {file_path}")
        return []

def generate_graph(metric_name, graph_title, filename, logs):
    """Generate a line chart from given logs for a specific metric."""

    # Dictionary to store logs grouped by server
    # Format: { "server_id": {"timestamps": [...], "values": [...]}, ... }
    server_data = {}

    # Loop through all logs
    for entry in logs:
        # Only consider entries that match the requested metric (e.g., "CPU", "RAM", etc.)
        if metric_name in entry["metric_type"]:
            server_id = entry["server_id"]  # Extract which server this log belongs to

            try:
                value = entry["value"]  # Extract the value (could be string or float)

                # Convert value to float: if it's a string with "%", remove it; else cast directly
                value = float(value.replace("%", "")) if isinstance(value, str) else float(value)

                # Convert timestamp string to a formatted string for graph x-axis (e.g., "22 Apr 14:33")
                timestamp = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S").strftime("%d %b %H:%M")

            except (ValueError, KeyError):
                # Skip any log with invalid value or missing keys
                continue

            # Initialize data structure for this server if not already present
            if server_id not in server_data:
                server_data[server_id] = {"timestamps": [], "values": []}

            # Add the timestamp and corresponding value to this server’s data
            server_data[server_id]["timestamps"].append(timestamp)
            server_data[server_id]["values"].append(value)

    # If no data has been collected, exit early
    if not server_data:
        print(f"No data found for metric '{metric_name}'")
        return

    # Get all unique timestamps across all servers, sorted
    # Then keep only the last 10 to avoid overcrowding the graph
    all_timestamps = []

    for server_entry in server_data.values():
        for ts in server_entry["timestamps"]:
            all_timestamps.append(ts)

    unique_sorted_timestamps = sorted(set(all_timestamps))
    all_timestamps = unique_sorted_timestamps[-10:]


    # Initialize a new Pygal line chart with rotated x-labels
    chart = pygal.Line(x_label_rotation=45)
    chart.title = graph_title  # Set the title of the chart
    chart.x_labels = all_timestamps  # Set common x-axis for all series

    # Add data line for each server
    for server_id, data in server_data.items():
        aligned = []  # List of values aligned with global timestamps
        for ts in all_timestamps:
            # Add the value if timestamp is present, otherwise insert None
            aligned.append(data["values"][data["timestamps"].index(ts)] if ts in data["timestamps"] else None)
        
        # Add this server's line to the chart
        chart.add(server_id, aligned)

    # Define where to save the chart
    output_path = os.path.join(output_folder, filename)

    # Render the chart to an SVG file
    chart.render_to_file(output_path)

    # Confirm to user
    print(f"Graph generated: {output_path}")
    
def generate_all_graphs():
    # 1. Load all logs
    all_logs = load_logs(local_file) + load_logs(serverb_file)
    local_logs = load_logs(local_file)
    remote_logs = load_logs(serverb_file)
    print(f"Loaded {len(remote_logs)} logs from both sources")

    # 2. Generate combined graphs (multi-server)
    generate_graph("CPU", "CPU Usage (All Servers)", "cpu_usage_combined.svg", all_logs)
    generate_graph("RAM", "RAM Usage (All Servers)", "ram_usage_combined.svg", all_logs)
    generate_graph("Disk", "Disk Usage (All Servers)", "disk_usage_combined.svg", all_logs)
    generate_graph("Processes", "Processes Count (All Servers)", "process_usage_combined.svg", all_logs)

    # 3. Generate Server A graphs
    generate_graph("CPU", "CPU - Local Machine", "cpu_usage_local.svg", local_logs)
    generate_graph("RAM", "RAM - Local Machine", "ram_usage_local.svg", local_logs)
    generate_graph("Disk", "Disk - Local Machine", "disk_usage_local.svg", local_logs)
    generate_graph("Processes", "Processes - Local Machine", "process_usage_local.svg", local_logs)

    # 4. Generate Server B graphs
    generate_graph("CPU", "CPU - Server B", "cpu_usage_serverb.svg", remote_logs)
    generate_graph("RAM", "RAM - Server B", "ram_usage_serverb.svg", remote_logs)
    generate_graph("Disk", "Disk - Server B", "disk_usage_serverb.svg", remote_logs)
    generate_graph("Processes", "Processes - Server B", "process_usage_serverb.svg", remote_logs)

# Run all
generate_all_graphs()