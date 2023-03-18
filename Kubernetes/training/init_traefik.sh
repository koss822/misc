#!/bin/bash
sudo snap install yq
microk8s kubectl get svc -n traefik traefik -o yaml > /root/traefik.yml
yq eval '.spec.ports[0].nodePort = 80' /root/traefik.yml -i
microk8s kubectl apply -f /root/traefik.yml
rm /root/traefik.yml