# See https://www.enigma14.eu/martin/blog/2018/10/24/aws-lambda-reboot-instance-when-http-unreachable-for-free/

import json
from botocore.vendored import requests
import boto3
import time
# e.g. eu-west-1
region = 'xx-xxxx-x'
instances = ['x-xxxxxxxxxxx']
website = 'https://www.enigma14.eu/'
webstring = 'SearchText'
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
    ec2 = boto3.client('ec2', region_name=region)
    ec2.reboot_instances(InstanceIds=instances)
