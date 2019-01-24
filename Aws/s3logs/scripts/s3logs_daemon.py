#!/usr/bin/env python3

# /usr/local/s3logs/s3logs_daemon.py
import mysql_s3logs, boto3, json, time

url = 'https://sqs.eu-west-1.amazonaws.com/QUEUE_ID/s3logs'
client = boto3.client('sqs')

def receive_messages():
    msgs = client.receive_message(QueueUrl=url)
    i=1
    while(msgs and 'Messages' in msgs.keys()):
        for msg in msgs['Messages']:
            body = json.loads(msg['Body'])
            mysql_s3logs.insert(body['id'], body['repository'],
                    time.strptime(body['date'], '%d/%b/%Y:%H:%M:%S +0000'),
                    body['ip'], body['item'][:200],
                    body['referer'][:200], body['agent'][:200])
            client.delete_message(QueueUrl=url,
                    ReceiptHandle=msg['ReceiptHandle'])
        msgs = client.receive_message(QueueUrl=url)
        print("Message %i received" % i)
        i+=1

while(True):
    try:
        receive_messages()
    except Exception as e:
        print('Error in parsing messages')
        print(e)
    print('Sleeping for 60 seconds')
    time.sleep(60)