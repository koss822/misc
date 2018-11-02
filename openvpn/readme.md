# OpenVPN script for generating client/server keys

The clients has static IP addresses and can communicate between them. Very usefull when you need to connect few computers behind NAT using OpenVPN server in cloud. All configuration is generated using genkey.sh script which uses YAML config. You can run genkey.sh multiple times without affecting current keys.

## Directory structure

    ├── clients
    │   ├── client1
    │   │   ├── client1.client.conf
    │   │   └── keys
    │   │       ├── ca.crt
    │   │       ├── client1.crt
    │   │       ├── client1.csr
    │   │       └── client1.key
    │   └── client2
    │       ├── client2.client.conf
    │       └── keys
    │           ├── ca.crt
    │           ├── client2.crt
    │           ├── client2.csr
    │           └── client2.key
    ├── genkey.py
    ├── server
    │   ├── ccd
    │   │   ├── client1
    │   │   └── client2
    │   ├── keys
    │   │   ├── ca.crt
    │   │   ├── ca.key
    │   │   ├── dh2048.pem
    │   │   ├── server.crt
    │   │   ├── server.csr
    │   │   └── server.key
    │   └── server.conf

## vpn.yml example structure

    ---
    server:
      fqdn: 'openvpn.server.com'
      port: '443'
      proto: 'udp'
      topology: '192.168.10.0 255.255.255.0'
    
    clients:
      - name: client1
        ip: 192.168.10.10
        subnet: 255.255.255.0
    
      - name: client2
        ip: 192.168.10.20
        subnet: 255.255.255.0
