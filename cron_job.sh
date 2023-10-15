#!/bin/bash

# Define the path to your Python script
SCRIPT_PATH="/home/karthickshiva1709_gmail_com/projects/ticketnew/main.py"

# Define the cron schedule (every 2 minutes)
CRON_SCHEDULE="*/2 * * * *"

# Check if the cron job already exists
if crontab -l | grep -q "$SCRIPT_PATH"; then
    echo "Cron job for the script already exists."
else
    # Add the cron job
    (crontab -l; echo "$CRON_SCHEDULE /usr/bin/python3 $SCRIPT_PATH") | crontab -
    echo "Cron job added for the script."
fi
