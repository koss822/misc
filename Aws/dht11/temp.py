#!/usr/bin/env python3
################################################################################
# Martin Konicek (c) 2019
# GNU/GPL
# mkonicek12@gmail.com
################################################################################
import sys
import Adafruit_DHT
import time
import boto3
import yaml
from sys import stdout

# Read and assign data from config file
CONFIG='/etc/temp.yaml'
data = yaml.load(open(CONFIG, 'r'), Loader=yaml.Loader)

SENSOR_PIN=data['sensor_pin']
NAMESPACE=data['namespace']
ACCESS_KEY=data['access_key']
SECRET_KEY=data['secret_key']
REGION=data['region']
LOG_GROUP=data['log_group']
LOG_STREAM=data['log_stream']

# Disable output console caching to see immediately logs in journal
def write_flush(args, w=stdout.write):
    w(args)
    stdout.flush()

def boto3_client(service):
    return boto3.client(
        service,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION
        )

def put_data(name, value):
    if value == None:
        log_data('Error 3002: Invalid try to read data from DHT11')
        raise Exception("Invalid value")

    print("For %s putting %s" % (name,value))
    print(cloudwatch.put_metric_data(
        MetricData=[ 
            {
                'MetricName': name,
                'Dimensions': [
                    {
                        'Name': 'SensorType',
                        'Value': 'DHT11'
                    }
                ],
                'Unit': "None",
                'Value': value
            }
        ],
        Namespace=NAMESPACE
    ))

def find_log_stream(streams):
    for stream in streams:
        if stream['logStreamName']==LOG_STREAM:
            return stream

def doesLogsExist():
    groups = logs.describe_log_groups(logGroupNamePrefix=LOG_GROUP)['logGroups']
    if len(groups)>0:
        for group in groups:
            if group['logGroupName'] == LOG_GROUP:
                return True
    return False

def start_logging():
    try:
        if not doesLogsExist():
            logs.create_log_group(logGroupName=LOG_GROUP)
            logs.create_log_stream(logGroupName=LOG_GROUP, logStreamName=LOG_STREAM)
        log_data("MSG 2005: DHT11 logger service started")
    except Exception as e:
        print("Cloudwatch Log error:")
        print(e)

def log_data(data):
    try:
        timestamp = int(round(time.time() * 1000))
        logEventArgs = {
            'logGroupName': LOG_GROUP,
            'logStreamName': LOG_STREAM,
            'logEvents': [
                {
                    'timestamp': timestamp,
                    'message': data
                }
            ]
        }

        # Find last log entry to continue with next log entry
        pretoken = find_log_stream(logs.describe_log_streams(logGroupName=LOG_GROUP, logStreamNamePrefix=LOG_STREAM)['logStreams'])
        if 'uploadSequenceToken' in pretoken:
            logEventArgs['sequenceToken'] = pretoken['uploadSequenceToken']

        response = logs.put_log_events(**logEventArgs)
        print('Uploading to logs: %s' % data)
        print(response)
    except Exception as e:
        print('Cloudwatch logs error:')
        print(e)


# Main code
stdout.write = write_flush # Disable output buffering
cloudwatch = boto3_client('cloudwatch')
logs = boto3_client('logs')
start_logging()

errors=0
while(True):
    try:
        humidity, temperature = Adafruit_DHT.read(11, SENSOR_PIN)
        put_data('Temperature', temperature)
        put_data('Humidity', humidity)
        log_data('MSG 4005: Succesfully read temperature and humidity')

    except Exception as e:
        print(e)
        if errors>2: # If 3 reads from DHT11 sensor fails
            log_data('Error 2222: Unable to read or send data')
            log_data(e)
            errors=0
        else:
            errors+=1
            time.sleep(60)
            continue

    time.sleep(1800) # sleep 30 minutes
