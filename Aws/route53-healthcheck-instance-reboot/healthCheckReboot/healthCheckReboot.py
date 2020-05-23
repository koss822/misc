import json
import os
import boto3
import time

env_vars = [
    'ALARM_NAME',
    'REGION',
    'INSTANCE_ID',
    'OUTPUT_SNS_ARN'
    ]

ENV = {}

for env_var in env_vars:
    ENV[env_var] = os.environ.get(env_var, None)
    if not ENV[env_var]:
        raise Exception(f"Environment variable {env_var} must be set!")
   
        
def reboot_instance(instanceID, regionName) -> "instanceID":
    """
    InstanceID
    instanceID - ID of instance
    regionName - name of region
    
    return InstanceID or False in case of exception
    """
    ec2 = boto3.resource('ec2', region_name=regionName)
    instance = ec2.Instance(instanceID)

    try:
        instance.stop()
        time.sleep(30)
        instance.stop(Force=True)
    except:
        pass
    
    for i in range(180): # wait 3 minutes
        instance = ec2.Instance(instanceID)
        if instance.state['Code'] == 80:
            break
        time.sleep(1)
    else:
        raise Exception('Unable to stop instance')
        
    instance.start()
    return instanceID
    
    
def notify_about_reboot(instanceID, snsarn) -> True:
    """
    Put SNS message about reboot to snsarn
    """
    client = boto3.client('sns', region_name='us-east-1')
    client.publish(TopicArn=snsarn, Message=f'EC2 instance {instanceID} was rebooted!')
    return True


def lambda_handler(event, context) -> "status about reboot":
    """
    event: see events/event.json 
    """
    print('EVENT:')
    print(event)
    for record in event.get('Records', None):
        sns = record.get('Sns', None)
        message = json.loads(sns.get('Message', None))
        msgalarm =  message.get('AlarmName', None)
        msgstatus = message.get('NewStateValue', None)
        
        if not all([sns,message,msgalarm,msgstatus]):
            continue
        
        if (msgalarm == ENV['ALARM_NAME']) and (msgstatus == 'ALARM'):
            notify_about_reboot(reboot_instance(ENV['INSTANCE_ID'], ENV['REGION']), ENV['OUTPUT_SNS_ARN'])
            return 'rebooting'
        else:
            return 'nothing to do'
            
    return 'no sns record found'
