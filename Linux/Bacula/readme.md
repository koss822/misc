# Bacula Backup Monitoring with InfluxDB and Grafana

## Overview
This project aims to monitor daily backup sizes from Bacula, storing the data in InfluxDB for time-series analysis and visualizing it in Grafana. The integration is done using a Python script scheduled with a daily cron job.

## Screenshot
![Screenshot](https://github.com/koss822/misc/raw/master/imgs/bacula-grafana.png)

## Project Components
- **Bacula**: Backup management system used to schedule and manage backup jobs.
- **InfluxDB**: Time-series database where backup sizes are stored.
- **Grafana**: Visualization tool used to create dashboards from the metrics stored in InfluxDB.
- **Cron Job**: Scheduler for executing the data collection script daily.

## Prerequisites
- Python 3.x
- Bacula installed and configured
- InfluxDB (version 2.x recommended)
- Grafana
- `influxdb-client` Python library

## Installation

### 1. Set Up InfluxDB
1. **Install InfluxDB**:
   Follow the [InfluxDB installation instructions](https://docs.influxdata.com/influxdb/v2.0/install/) for your platform.
   
2. **Create a Bucket**:
   Access the InfluxDB UI and create a bucket named `bacula`.

3. **Create an Access Token**:
   - Navigate to `Data` > `Tokens`.
   - Click on `+ Create Token`, select `Read/Write Token`, choose your organization and the bucket, and provide it a name. **Copy the token** for later use.

### 2. Set Up Grafana
1. **Install Grafana**:
   Follow the [Grafana installation guide](https://grafana.com/docs/grafana/latest/installation/) for your platform.
 
2. **Add InfluxDB Data Source**:
   - Go to `Configuration` > `Data Sources` > `Add Data Source`.
   - Choose `InfluxDB`, and provide the necessary details using the token created earlier. Set the bucket and other required fields.
   - Click on `Save & Test` to ensure the connection is successful.

3. **Grafana influx query**
```
from(bucket: "bacula")
|> range(start: -7d) 
|> group(columns: ["size"])
```

### 3. Set Up Python Script
1. **Dependencies**:
   Install the needed Python libraries:
   ```bash
   pip install influxdb-client
   ```