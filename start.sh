#!/bin/bash

PROCESS_NAME="main.py"
CONTAINER_NAME="postgres"
LOG_FILE="/var/log/finanzas_app/app.log"

if [ ! "$(docker ps -q -f name=${CONTAINER_NAME})" ]; then
    docker compose up -d
fi

if ! pgrep -f "$PROCESS_NAME" > /dev/null ; then
    nohup python3 main.py > $LOG_FILE 2>&1 &
    echo "- Start app. Logs in $LOG_FILE"
    echo "- Running on http://127.0.0.1:5000"
else
    echo "- App already started. Doing nothing"
fi
