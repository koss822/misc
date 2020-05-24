# AWS scripts and tools

## [route53-healthcheck-instance-reboot](https://github.com/koss822/misc/blob/master/Aws/route53-healthcheck-instance-reboot/)
### Description
This is a SAM application which watches Route53 HealthCheck and when it goes to ALARM state it reboots specified ec2 instance.

### Diagram
![Screenshot](https://github.com/koss822/misc/raw/master/imgs/heathcheck/route53-healthcheck-reboot.png "Route53 HealthCheckReboot screenshot")

## [RaspberryPi tools for DHT11](https://github.com/koss822/misc/blob/master/Aws/dht11/)

DHT11 utilities for Raspberry Pi works very straigtforward. At first you connect DHT11 sensor to RaspberryPi and edit /etc/temp.yaml (you need to modify PIN where you connected VOut of your DHT11 sensor).

After that you install utilities on your RaspberryPi and also modify AWS API KeyPair which you firstly create in AWS IAM with ability to put Cloudwatch events and metrics.

Then you are ready. Once you start a "temp" service you it will upload your metric to AWS Cloudwatch. Also on each measurement there will be uploaded logs about success or failure. I strongly recommend to create a Cloudwatch alarm which watch keyword "success" in logs and if there are less than 1 success per hour I would recommend sending an alert to your e-mail address to inform you that there are errors in measurement (e.g. sensor or raspberry pi is broken).

### Screenshot
![Screenshot](https://github.com/koss822/misc/blob/master/imgs/aws-dht11.png?raw=true "DHT11 Cloudwatch screenshot")

## [HTTP HealthCheck Reboot Tool](https://github.com/koss822/misc/blob/master/Aws/website_check/)

This is a very simple lambda script for rebooting EC2 instance when HTTP(s) site is unreachable or does not contain selected text.

When you create this Lambda script in AWS you should trigger it by _CloudWatch Events_ trigger with _Schedule expression_ set up for _rate(1 hour)_ or whatever you like. For most scenarios it should run completely free of charge in free tier usage.

It is also needed to increase timeout for this script - recommended value is 10 minutes but might be lower.

**NEW 2019**
I have created a CloudFormation template for you with prepublicated Lambda source code in S3 bucket. Everything what you need to do is deploy cloudformation template with Parameters (SNS topics which you create yourself for alerting, instance ID, region) and you are ready!

### Diagram
![HTTP Health Check](https://raw.githubusercontent.com/koss822/misc/master/imgs/http_health_check.png "HTTP Health Check diagram")

## [AWS APC Ups state of lose power publisher](https://github.com/koss822/misc/blob/master/Aws/apcupsarn/)

I was solving issue that I wanted to know when my UPS lose and restore power. First idea was to use some kind of e-mail but it is very difficult to configure to pass your message through SPAM folder etc. Using SNS (Simple Notification Service) within AWS is so much more easier. You just use Python three liner to publish message to ARN queue and then SNS publish it to your e-mail, SMS or whatever of your choice.

### Diagram
![UPS](https://raw.githubusercontent.com/koss822/misc/master/imgs/ups.png "UPS diagram")

## [S3Logs](https://github.com/koss822/misc/tree/master/Aws/s3logs)

This tools watches logs directory where are the S3 Logs files stored with Lambda script located in _aws_ directory and when there is triggered S3 bucket event - _ObjectCreated_ on directory where S3 logs are stored the lambda script creates the message in SQS (Simple Queue Service) and delete log file.

After that there is running SystemD daemon on Linux machine with MySQL installed called s3logs_daemon.py (stored in _scripts_ directory) which check SQS queue for new logs and insert them into MySQL database.

Please be informed that there is no frontend - the main reason is that I find using PHPMyAdmin more universal and better because I can create directly SQL queries which I like.

### Diagram
![S3 Logs diagram](https://raw.githubusercontent.com/koss822/misc/master/imgs/sqss3.png "S3 Logs diagram")

### Installation

_some image tutorial is stored in_ [imgs directory](https://github.com/koss822/misc/tree/master/Aws/s3logs/imgs)

1. Clone repository to your directory
2. Set-up S3 logs in directory you like
3. Create lambda function (source file is stored in _aws_ directory) which is triggered by CloudWatch event _ObjectCreated_ on S3 Logs directory.
4. Set-up SQS queue
5. Wait few hours (S3 logs are created only every few hours not on every access)
6. Check SQS queue that it contains messages
7. Install MySQL, PhpMyAdmin, Apache
8. Create database with initial structure (sql file is in the _scripts_ directory)
9. Install scripts and SystemD service files
10. Start and enable SystemD service

Of course do not forget to change variables in various script files. Also the path where scripts should be installed is visible in the source files.
