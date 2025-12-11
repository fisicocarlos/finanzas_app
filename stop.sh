#!/bin/bash 

PROCESS_NAME="main.py"
CONTAINER_NAME="postgres"

if pgrep -f "$PROCESS_NAME" > /dev/null ; then
    echo "- Kill python process"
    pkill -f "$PROCESS_NAME"
else
    echo "- App already stopped. Doing nothing"
fi

if docker ps -q -f name=${CONTAINER_NAME} >/dev/null ; then
    echo "- Stopping postgres container"
    docker stop ${CONTAINER_NAME} > /dev/null
fi

