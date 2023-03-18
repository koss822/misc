#!/bin/bash
# Do not forget to rm -rf /var/lib/cloud
export HOME="/home/ubuntu/"
cd /home/ubuntu/misc/Kubernetes/training/
git config --global --add safe.directory /home/ubuntu/misc
git pull
sleep 120
bash kubeinit.sh