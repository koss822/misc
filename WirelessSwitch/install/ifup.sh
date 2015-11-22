#!/bin/bash

# Never route local traffic through 3G dongle
ip route add table 42 default via 192.168.0.1
ip rule add from 192.168.0.0/24 table 42

# Always route this ip for connectivity testing through cable connection
ip route add 4.2.2.2/32 via 192.168.0.1 dev eth0
