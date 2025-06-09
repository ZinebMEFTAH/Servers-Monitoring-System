#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
import os
import json

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "meftahworld@gmail.com"
EMAIL_PASSWORD = "ueeulogtrmzdhnyu"
EMAIL_RECEIVER = "meftahworld@gmail.com"

# Pathsa
storage_folder = os.path.join(os.path.dirname(__file__), "../storage")
alerts_file = os.path.join(storage_folder, "alerts_log.json")
template_path = os.path.join(os.path.dirname(__file__), "../config/email_template.txt")

def load_email_template():
    """Loads the email template from file."""
    if not os.path.exists(template_path):
        return "CRISIS ALERT \nServer: {{server}}\nIssue: {{metric}} exceeded the threshold!\nCurrent Value: {{value}}%\nDetected at: {{timestamp}}\nPlease take immediate action."
    
    with open(template_path, "r") as file:
        return file.read()

def save_alert_to_json(server, metric, value, timestamp):
    """Save the alert details in alerts_log.json without enforcing limits."""
    print(server)
    alert_entry = {
        "server": server,
        "metric": metric,
        "value": value,
        "timestamp": timestamp
    }

    # Ensure the storage folder exists
    if not os.path.exists(storage_folder):
        os.makedirs(storage_folder)

    # Load existing alerts (fix for empty or corrupted file)
    if os.path.exists(alerts_file):
        try:
            with open(alerts_file, "r") as file:
                alerts = json.load(file)
                if not isinstance(alerts, list):  # Ensure it's a list
                    alerts = []
        except (json.JSONDecodeError, FileNotFoundError):
            alerts = []
    else:
        alerts = []

    # Append new alert entry
    alerts.append(alert_entry)

    print(alerts)
    # Save updated alerts back to JSON (ensuring valid formatting)
    with open(alerts_file, "w") as file:
        json.dump(alerts, file, indent=4)

    print(f"Alert logged successfully: {alert_entry}")


def send_email_alert(server, metric, value, timestamp):
    """Sends an email alert and stores it in alerts_log.json."""
    template = load_email_template()
    message_body = template.replace("{{server}}", server)\
                           .replace("{{metric}}", metric)\
                           .replace("{{value}}", str(value))\
                           .replace("{{timestamp}}", timestamp)
    # Save alert to JSON
    save_alert_to_json(server, metric, value, timestamp)
    msg = MIMEText(message_body)
    msg["Subject"] = "CRISIS DETECTED on Server!"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        print("Sending email alert...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        # TLS encryption
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")