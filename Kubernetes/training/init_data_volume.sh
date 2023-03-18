#!/bin/bash

# Check if LVM VG kube-data exists
if sudo vgdisplay | grep -q kube-data; then
    echo "LVM VG kube-data already exists"
else
    echo "LVM VG kube-data does not exist, creating..."
    sudo pvcreate /dev/xvdf
    sudo vgcreate kube-data /dev/xvdf
    echo "LVM VG kube-data has been created"
fi

