#!/usr/bin/env python3

import os
import json
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Paths
storage_folder = os.path.join(os.path.dirname(__file__), "../storage")
json_file = os.path.join(storage_folder, "system_logs.json")
alerts_file = os.path.join(storage_folder, "alerts_log.json")
graphs_folder = os.path.join(os.path.dirname(__file__), "../graphs")
remote_file = os.path.expanduser("~/AMS_Project/storage/remote/serverb_logs.json")

# Function to fetch logs from Server B
def fetch_serverb_logs():
    remote_user = "serverb"  # ← your Server B username
    remote_ip = "192.168.64.12"  # ← Server B IP address
    remote_path = "/home/serverb/AMS_Project/storage/system_logs.json"  # ← path on Server B
    os.makedirs(os.path.dirname(remote_file), exist_ok=True)
    os.system(f"scp {remote_user}@{remote_ip}:{remote_path} {remote_file}")
    print("Server B logs fetched.")

# Load combined logs from Server A and Server B
def load_logs():
    fetch_serverb_logs()  # Always fetch latest logs from Server B

    logs = []

    # Load Server A logs
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            try:
                logs += json.load(file)
            except json.JSONDecodeError:
                pass

    # Load Server B logs
    if os.path.exists(remote_file):
        with open(remote_file, "r") as file:
            try:
                logs += json.load(file)
            except json.JSONDecodeError:
                pass

    # Sort and return latest 10 logs
    logs = sorted(logs, key=lambda x: x["timestamp"])
    return logs[-10:]

# Load alerts
def load_alerts():
    if not os.path.exists(alerts_file):
        return []
    with open(alerts_file, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

# Homepage
@app.route("/")
def index():
    logs = load_logs()
    alerts = load_alerts()
    graphs = [f for f in os.listdir(graphs_folder) if f.endswith(".svg")]

    # Group graphs
    combined_graphs = sorted([g for g in graphs if "combined" in g])
    local_graphs = sorted([g for g in graphs if "local" in g])
    serverb_graphs = sorted([g for g in graphs if "serverb" in g])

    return render_template("index.html",
                           logs=logs,
                           alerts=alerts,
                           combined_graphs=combined_graphs,
                           local_graphs=local_graphs,
                           serverb_graphs=serverb_graphs)

# Graph route
@app.route("/graphs/<path:filename>")
def serve_graph(filename):
    return send_from_directory(graphs_folder, filename)

# Launch
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)
    # debug=True = server automatically reloads when you make changes to the code