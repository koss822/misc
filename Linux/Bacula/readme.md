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

## Diagram
```
 +-----------------+          +---------------------+
 |     Bacula      | ----->   |    Bacula Logs      |
 |    (Backup)     |          |                     |
 +-----------------+          +---------------------+
                                   |
                                   |
                                   v
                   +----------------------------------+
                   | Data Collection Script           |
                   | (bacula-influx.py)               |
                   +----------------------------------+
                                   |
                                   |
                                   v
                   +---------------------+
                   |      InfluxDB       |
                   |   (Time-Series DB)  |
                   +---------------------+
                                   |
                                   |
                                   v
                   +---------------------+
                   |      Grafana        |
                   |   (Visualization)   |
                   +---------------------+
```


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

# check_bacula_director.sh

`check_bacula_director.sh` is a simple Nagios plugin script to monitor the Bacula Director process. It checks if the `bacula-dir` process is running and returns appropriate status codes for Nagios.

## Features
- Verifies if the Bacula Director process (`bacula-dir`) is running.
- Outputs Nagios-compatible status messages:
- **OK**: If the Bacula Director is running.
- **CRITICAL**: If the Bacula Director is not running.

---

## Prerequisites
- Ensure `pgrep` is installed on the system (commonly available on most Linux distributions).
- The Nagios user must have permission to execute the script.

---

## Installation

1. Save the script as `check_bacula_director.sh` in your Nagios plugins directory (e.g., `/usr/lib/nagios/plugins/`).

2. Make the script executable:

```chmod +x /usr/lib/nagios/plugins/check_bacula_director.sh```

---

## Usage

The script checks if the `bacula-dir` process is running. If it is, it outputs an "OK" message; otherwise, it outputs a "CRITICAL" message.

### Command Line Example
Run the script manually to test:

```./check_bacula_director.sh```


Expected output:
- **If Bacula Director is running**:  

OK: Bacula Director is running.

- **If Bacula Director is not running**:  

CRITICAL: Bacula Director is not running!

Exit codes:
- `0`: OK
- `2`: CRITICAL

---

## Nagios Configuration

To integrate this script into Nagios, follow these steps:

### Step 1: Define Command in `commands.cfg`
Add the following command definition to your Nagios `commands.cfg` file:

```
define command {
command_name check_bacula_director
command_line /usr/lib/nagios/plugins/check_bacula_director.sh
}
```

### Step 2: Define Service in Your Host Configuration
Add a service definition to monitor the Bacula Director in your host's configuration file:

```
define service {
use generic-service ; Inherit default service settings
host_name your_host_name ; Replace with your host's name
service_description Bacula Director Status
check_command check_bacula_director
}
```

### Step 3: Restart Nagios
Apply the changes by restarting Nagios:

```sudo systemctl restart nagios```

---

## Example Output in Nagios Web Interface

- **Service Name**: Bacula Director Status  
- **Status**: OK or CRITICAL (depending on whether the process is running).  
- **Output**:  
  - OK: "Bacula Director is running."  
  - CRITICAL: "Bacula Director is not running!"

---

## Troubleshooting

1. **Permission Issues**:
   Ensure the script has executable permissions and that the Nagios user can access it.

2. **Incorrect Path**:
   Verify that the path to `check_bacula_director.sh` in `commands.cfg` matches its actual location.

3. **Bacula Process Name**:
   If `bacula-dir` runs under a different name, update the script to reflect this.

---

## License

This script is open-source and can be freely modified and distributed under the MIT License.