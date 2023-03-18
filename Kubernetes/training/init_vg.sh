#!/bin/bash
vgcfgrestore -y /dev/kube-data
vgchange -ay /dev/kube-data
