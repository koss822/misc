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


### Known issues

Currently botocore.vendored library with requests is obsolete. I have created a requests layer with this fix. You can install layer with these commands. Don't forget to attach layer to function. I will make some better solution soon.

```
cd requests_layer/
sudo pip3 install --target . requests
zip -r ../requests_layer.zip .
cd ..
aws --profile admin --region eu-west-1 s3 cp requests_layer.zip s3://aws-public/
aws --profile admin --region eu-west-1 lambda publish-layer-version --layer-name requests --content S3Bucket=aws-public,S3Key=requests_layer.zip --compatible-runtimes python3.8
```
