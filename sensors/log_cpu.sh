#!/bin/bash

# Get CPU usage (Ubuntu/Linux version)
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8}')
# -b = batch mode 
# -n1 = one iteration
# grep = filters
# awk = processing tool

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Call Python function to log data using full path
python3 -c "import sys; sys.path.append('$SCRIPT_DIR'); from log_data import log_data; log_data('CPU', $CPU_USAGE)"
# -c means “run the following commands as a program.”

echo "✅ CPU logged: $CPU_USAGE%"