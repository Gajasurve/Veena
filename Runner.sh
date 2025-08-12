#!/bin/bash


LOG_FILE="logfile.log"


echo "$(date) - Script started." >> "$LOG_FILE"


node Chakra.js &
NODE_PID=$!


echo "$(date) - Node process started with PID: $NODE_PID" >> "$LOG_FILE"


sleep 120


kill $NODE_PID


if ps -p $NODE_PID > /dev/null; then
    echo "$(date) - Process $NODE_PID is still running after sleep. Killing it now." >> "$LOG_FILE"
    kill $NODE_PID
else
    echo "$(date) - Process $NODE_PID has already been terminated." >> "$LOG_FILE"
fi


echo "$(date) - Script completed." >> "$LOG_FILE"
