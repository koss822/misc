from __future__ import print_function
import json, boto3, os, sys, uuid, re, hashlib
     
s3_client = boto3.client('s3')
s3 = boto3.resource('s3')
url = 'https://sqs.eu-west-1.amazonaws.com/YOUR_ID/s3logs'
client = boto3.client('sqs')

def send_message(message):
    print(client.send_message(QueueUrl=url, MessageBody=message)) 
    
def create_json(id, repository, date, ip, item, referer, agent):
    return json.dumps({
        'id': id,
        'repository': repository,
        'date': date,
        'ip': ip,
        'item': item,
        'referer': referer,
        'agent': agent
        })


def parse_body(body):
    try:
        regex = '(\w+) ([\w_-]+) \[(.*?)\] ([(\d\.)]+) - (\w+) ([\w\.]*) (.+?) "(.*?)" (\d+) - (\d+) (\d+) (\d+) (\d+) "(.*?)" "(.*?)" -'

        match = re.match(regex, body).groups()

        id = hashlib.sha224(body.encode('utf-8')).hexdigest()
        repository = match[1]
        date = match[2]
        ip = match[3]
        item = match[6]
        referer = match[13]
        agent = match[14]

        return create_json(id, repository, date, ip, item, referer, agent)

    except Exception as e:
        print(e)
    
def lambda_handler(event, context):
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']
    obj = s3.Object(bucket, key)
    for body in obj.get()['Body'].read().decode('utf-8').split('\n'):
        try:
            send_message(parse_body(body))
        except:
            pass  