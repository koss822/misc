# My Home Server Setup with Kubernetes (MicroK8s) on Ubuntu

## Overview

This README provides an overview of my home server setup, which runs on Ubuntu using MicroK8s (a lightweight Kubernetes distribution). The setup includes various tools and applications for monitoring, media management, development, and more.

## Core Components
### Ubuntu Server
*The base operating system running all services.*

### MicroK8s
*A lightweight, CNCF certified Kubernetes distribution that's easy to install and maintain on Ubuntu.
Kubernetes (K8s)*

## Monitoring and Observability
### Grafana
*Data visualization and monitoring*

### Prometheus
*Monitoring and alerting toolkit*

### [Loki](loki.md) 
*Log aggregation system*

<img src="https://raw.githubusercontent.com/koss822/misc/master/imgs/loki1.png" alt="loki" />


### Promtail
*Log collector for Loki*

### InfluxDB
*Time series database*

### Telegraf
*Server agent for collecting metrics*

## Networking and Security
### Traefik
*Cloud native edge router*

### WireGuard
*VPN for secure remote access*

## Development and Databases
### MariaDB
*Relational database*

### MongoDB
*NoSQL database*

### phpMyAdmin
*Web interface for MySQL/MariaDB*

### Node-RED
*Flow-based development tool*

## Additional Services
### Nagios
*IT infrastructure monitoring*

### Smokeping
*Network latency monitoring*

### Docker Registry
*Private container image registry*

### MediaWiki
*Wiki platform*

### LibreChat
*Open-source chat platform*

## Conclusion

This home server setup leverages the power of Kubernetes (MicroK8s) on Ubuntu to create a flexible, scalable, and robust environment for various services and applications. From monitoring and development tools to media management and custom applications, this setup demonstrates the versatility of a containerized infrastructure for home use.

## Diagram
<img src="https://raw.githubusercontent.com/koss822/misc/master/imgs/diagrams/homesetup.drawio.png" alt="diagram" />