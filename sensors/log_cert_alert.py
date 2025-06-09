#!/usr/bin/env python3

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import feedparser
import json
import os
from datetime import datetime

# RSS feed URL
CERT_RSS_URL = "https://www.cert.ssi.gouv.fr/feed"

# JSON file path
storage_folder = os.path.join(os.path.dirname(__file__), "../storage")
json_file = os.path.join(storage_folder, "system_logs.json")
os.makedirs(storage_folder, exist_ok=True)

SERVER_ID = "cert"
MAX_LOG_ENTRIES = 100

def fetch_latest_cert_alert():
    # Parse RSS feed
    feed = feedparser.parse(CERT_RSS_URL)
    if not feed.entries:
        print("No CERT alerts found.")
        return

    latest = feed.entries[0]

    try:
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print("Failed to parse published date.")
        return

    alert_entry = {
        "server_id": SERVER_ID,
        "metric_type": f"Security Alert: {latest.title}",
        "timestamp": timestamp_str,
        "value": latest.link
    }

    # Load existing data
    data = []
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass

    # Avoid duplicates (by link)
    if any(entry["value"] == alert_entry["value"] for entry in data):
        print("Alert already exists, skipped.")
        return

    # Append and trim
    data.append(alert_entry)
    
    with open(json_file, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"New CERT alert logged: {latest.title}")

if __name__ == "__main__":
    fetch_latest_cert_alert()