import json
from botocore.vendored import requests
import boto3
import time
import os

region = os.environ.get('region')
instanceID = os.environ.get('instanceID')
website = os.environ.get('website')
webstring = os.environ.get('webstring')
snsarn = os.environ.get('snsarn')

def lambda_handler(event, context):
    for i in range(0,3):
        if check_website():
            return 'Website OK'
        time.sleep(60)
    reboot_instance()
    return 'Restarted instances'
        
    
def check_website():
    r = requests.get(website)
    if webstring in r.text:
        return True
    else:
        return False

def reboot_instance():
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instanceID)
    instance.stop()
    time.sleep(30)
    try:
        instance.stop(Force=True)
    except:
        pass
    while(instance.state['Code'] != 80):
        time.sleep(1)
    instance.start()
    client = boto3.client('sns')
    client.publish(TopicArn=snsarn, Message='EC2 instance rebooted!')