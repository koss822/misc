# HTTP HealthCheck Reboot Tool

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
