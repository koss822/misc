#!/bin/bash
sudo chown ubuntu:ubuntu -R /home/ubuntu
sudo snap remove microk8s
sudo lvremove -y /dev/kube-data/*
sudo snap install microk8s --classic
microk8s stop
echo "--service-node-port-range=0-65535" >> /var/snap/microk8s/current/args/kube-apiserver
microk8s start
microk8s enable dns
microk8s enable community
microk8s enable traefik
microk8s helm repo add openebs-lvmlocalpv https://openebs.github.io/lvm-localpv
microk8s helm repo add bitnami https://charts.bitnami.com/bitnami
microk8s helm delete lvm-localpv
microk8s helm delete wordpress
/home/ubuntu/misc/Kubernetes/training/init_data_volume.sh
/home/ubuntu/misc/Kubernetes/training/init_openebs.sh
/home/ubuntu/misc/Kubernetes/training/init_sc.sh
/home/ubuntu/misc/Kubernetes/training/init_traefik.sh
/home/ubuntu/misc/Kubernetes/training/init_wordpress_helm.sh
