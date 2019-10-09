# APC UPS ARN message sender

## Description

I was solving issue that I wanted to know when my UPS lose and restore power. First idea was to use some kind of e-mail but it is very difficult to configure to pass your message through SPAM folder etc. Using SNS (Simple Notification Service) within AWS is so much more easier. You just use Python three liner to publish message to ARN queue and then SNS publish it to your e-mail, SMS or whatever of your choice.

## Installation
1. Copy onbattery and offbattery files to /etc/apcupsd/
2. Modify ARN queue in files and makes them executable
3. Create credential and config files for user root under .aws directory - https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
4. Make sure that credentials can publish into your queue

## Diagram
![UPS](https://raw.githubusercontent.com/koss822/misc/master/imgs/ups.png "UPS diagram")
