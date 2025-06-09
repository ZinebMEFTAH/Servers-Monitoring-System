#!/bin/bash

# Get Disk usage (Ubuntu/Linux version)
DISK_USAGE=$(df -h / | awk 'NR==2 {gsub("%",""); print $5}')
# df = disk free for all filesystem mounted partitions
# / = root partition
# -h = human readable
# NR = the line to be processed

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Call Python function to log data using full path
python3 -c "import sys; sys.path.append('$SCRIPT_DIR'); from log_data import log_data; log_data('Disk', $DISK_USAGE)"
# -c means “run the following commands as a program.”

echo "✅ Disk logged: $DISK_USAGE%"