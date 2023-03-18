#!/bin/bash

# Check if Helm chart for WordPress is installed
if microk8s helm list | grep -q wordpress; then
    echo "Helm chart for WordPress is installed"
else 
    echo "Helm chart for WordPress is not installed"
    # Get public DNS of EC2 instance
    PUBLIC_DNS=$(curl -s http://169.254.169.254/latest/meta-data/public-hostname)

    cp /home/ubuntu/misc/Kubernetes/training/wordpress.yml /tmp/wordpress.yml
    
    # Replace "HOSTREPLACE" with public DNS in wordpress.yml
    sed -i "s/HOSTREPLACE/$PUBLIC_DNS/g" /tmp/wordpress.yml
    
    # Deploy WordPress using modified values file
    microk8s helm upgrade --install wordpress bitnami/wordpress -f /tmp/wordpress.yml
    echo "Helm chart for WordPress is installed"
fi
