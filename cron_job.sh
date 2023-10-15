#!/bin/bash

# Define the project path
PROJECT_PATH="~/projects/ticketnew"

# Define the path to your Python script
SCRIPT_PATH="./main.py"  # Relative path within the project directory

# Define the cron schedule (every 2 minutes)
CRON_SCHEDULE="*/2 * * * *"

# Define the path to the output log file (relative to the project directory)
LOG_FILE="./cron_output.log"

# Check if the cron job already exists
if crontab -l | grep -q "$PROJECT_PATH/$SCRIPT_PATH"; then
    echo "Cron job for the script already exists."
else
    # Add the cron job with output redirection to the log file
    (crontab -l; echo "$CRON_SCHEDULE cd $PROJECT_PATH && /usr/bin/python3 $SCRIPT_PATH >> $LOG_FILE 2>&1") | crontab -
    echo "Cron job added for the script with output to $PROJECT_PATH/$LOG_FILE."
fi
