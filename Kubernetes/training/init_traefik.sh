#!/bin/bash
sudo snap install yq
microk8s kubectl get svc -n traefik traefik -o yaml > ~/traefik.yml
yq eval '.spec.ports[0].nodePort = 80' ~/traefik.yml -i
microk8s kubectl apply -f ~/traefik.yml
rm ~/traefik.yml
