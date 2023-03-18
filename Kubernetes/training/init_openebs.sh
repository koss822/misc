#!/bin/bash

# Check if Helm chart for WordPress is installed
if microk8s helm list | grep -q lvm-localpv; then
    echo "Helm chart for OpenEBS is installed"
else 
    echo "Helm chart for OpenEBS is not installed"
    microk8s helm install lvm-localpv openebs-lvmlocalpv/lvm-localpv -f /home/ubuntu/misc/Kubernetes/training/lvm-localpv.yml
    
    sleep 60
    echo "Helm chart for OpenEBS is installed"
fi
