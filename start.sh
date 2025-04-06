#!/bin/bash

# Script to start WSO2 API Manager

# Path to WSO2 API Manager directory
API_M_HOME="/path/to/wso2am"  # Update this path

# Verify the directory exists
if [ ! -d "$API_M_HOME" ]; then
  echo "Error: WSO2 API Manager directory not found at $API_M_HOME"
  exit 1
fi

# Start the server in the background
echo "Starting WSO2 API Manager..."
"$API_M_HOME/bin/wso2server.sh" start

# Check if the server started
if [ $? -eq 0 ]; then
  echo "WSO2 API Manager started successfully."
else
  echo "Error: Failed to start WSO2 API Manager."
  exit 1
fi