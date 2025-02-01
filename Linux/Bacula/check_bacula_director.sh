#!/bin/bash

# Check if Bacula Director is running
if pgrep -x "bacula-dir" > /dev/null; then
    echo "OK: Bacula Director is running."
    exit 0
else
    echo "CRITICAL: Bacula Director is not running!"
    exit 2
fi