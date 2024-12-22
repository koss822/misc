#!/bin/bash

# Script to find the Kubernetes pod associated with a process (PID)

# Check if a PID is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <PID>"
    exit 1
fi

# Get the PID from the first argument
PID=$1

# Verify the process exists
if [[ ! -d "/proc/$PID" ]]; then
    echo "Error: Process with PID $PID does not exist."
    exit 1
fi

# Extract the cgroup information for the process
CGROUP_FILE="/proc/$PID/cgroup"
if [[ ! -f $CGROUP_FILE ]]; then
    echo "Error: Unable to access cgroup information for PID $PID."
    exit 1
fi

# Extract the container ID (last segment of the cgroup path)
CONTAINER_ID=$(cat "$CGROUP_FILE" | awk -F '/' '{print $NF}' | tr -d '\n')

# Check if we got a valid container ID
if [[ -z "$CONTAINER_ID" || ${#CONTAINER_ID} -lt 64 ]]; then
    echo "Error: Unable to determine container ID for PID $PID."
    exit 1
fi

echo "Container ID: $CONTAINER_ID"

# Use kubectl to find the pod corresponding to the container ID
POD_INFO=$(kubectl get pods --all-namespaces -o json | jq -r \
    --arg CONTAINER_ID "$CONTAINER_ID" \
    '.items[]
    | select(.status.containerStatuses != null)
    | select(.status.containerStatuses[].containerID? != null and (.status.containerStatuses[].containerID | endswith($CONTAINER_ID)))
    | "\(.metadata.namespace) \(.metadata.name)"')

# Output the result
if [[ -z "$POD_INFO" ]]; then
    echo "Error: No pod found for container ID $CONTAINER_ID."
    exit 1
else
    echo "Pod Information:"
    echo "Namespace: $(echo $POD_INFO | awk '{print $1}')"
    echo "Name: $(echo $POD_INFO | awk '{print $2}')"
fi