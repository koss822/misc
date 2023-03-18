#!/bin/bash

echo "Applying StorageClass"
microk8s kubectl apply -f /home/ubuntu/misc/Kubernetes/training/sc.yml
