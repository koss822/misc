#!/usr/bin/python
import re
import os
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from pprint import pprint

# Configuration for InfluxDB
INFLUXDB_URL = 'http://influxdb'
INFLUXDB_TOKEN = ''
INFLUXDB_ORG = 'influxdata' 
INFLUXDB_BUCKET = 'bacula'

# Path to Bacula log
BACULA_LOG_PATH = '/var/log/bacula/bacula.log'
# Temporary file to keep track of processed job IDs
PROCESSED_IDS_FILE = '/home/user/processed_ids.txt'

client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Load processed job IDs
if os.path.exists(PROCESSED_IDS_FILE):
    with open(PROCESSED_IDS_FILE, 'r') as f:
        processed_ids = set(line.strip() for line in f)
else:
    processed_ids = set()

new_entries = []

with open(BACULA_LOG_PATH, 'r') as log_file:
    lines = log_file.readlines()
    for i in range(len(lines)):
        line = lines[i]
        
        # Check for job completion line
        job_match = re.search(r'\s+JobId (\d+): .*?Backup (.*?)$', line)
        if job_match:
            job_id = job_match.group(1)
            job_name = job_match.group(2)
            if job_id not in processed_ids:
                size_bytes = None
                end_time = None

                # Look for FD Bytes Written and End time in the following lines
                for j in range(i + 1, len(lines)):
                    size_match = re.search(r'\s+FD Bytes Written:\s+([\d,]+)', lines[j])
                    end_time_match = re.search(r'\s+End time:\s+(.*)', lines[j])

                    if size_match:
                        size_bytes = int(size_match.group(1).replace(',', ''))

                    if end_time_match:
                        end_time_str = end_time_match.group(1).strip()
                        end_time = datetime.strptime(end_time_str, '%d-%b-%Y %H:%M:%S').isoformat()

                    # Stop searching after both pieces of information are found
                    if size_bytes is not None and end_time is not None:
                        break

                # If we've gathered the necessary information, prepare to send it to InfluxDB
                if size_bytes is not None and end_time is not None:
                    entry = {
                        'job_id': job_id,
                        'job_name': job_name,
                        'size': size_bytes,
                        'end_time': end_time
                    }
                    new_entries.append(entry)
                    # Add job ID to processed IDs
                    processed_ids.add(job_id)

# Send the new entries to InfluxDB
for entry in new_entries:
    point = (
        Point("bacula_backup")
        .tag("job_id", entry['job_id'])
        .tag("job_name", entry['job_name'])
        .field("size", entry['size'])
        .time(entry['end_time'])
    )
    try:
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        # Update the processed IDs file
        with open(PROCESSED_IDS_FILE, 'w') as f:
            for job_id in processed_ids:
                f.write(f"{job_id}\n")
        print(f"Successfully written: {entry}")  # Log success
    except Exception as e:
        print(f"Error writing entry: {entry}, Error: {e}")

print(f"Processed {len(new_entries)} new entries.")
