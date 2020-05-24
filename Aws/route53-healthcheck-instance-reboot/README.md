# route53-healthcheck-instance-reboot

## Diagram
![Screenshot](https://github.com/koss822/misc/raw/master/imgs/heathcheck/route53-healthcheck-reboot.png "Route53 HealthCheckReboot screenshot")

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- healthCheckReboot - Code for the application's Lambda function.
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an SNS and Route53 HealthCheck. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modified IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name route53-healthcheck-instance-reboot
```

## Installation
![Screenshot](https://github.com/koss822/misc/raw/master/imgs/heathcheck/healthcheck1.PNG "Route53 HealthCheckReboot screenshot")
![Screenshot](https://github.com/koss822/misc/raw/master/imgs/heathcheck/healthcheck2.PNG "Route53 HealthCheckReboot screenshot")
![Screenshot](https://github.com/koss822/misc/raw/master/imgs/heathcheck/healthcheck3.PNG "Route53 HealthCheckReboot screenshot")
![Screenshot](https://github.com/koss822/misc/raw/master/imgs/heathcheck/healthcheck4.PNG "Route53 HealthCheckReboot screenshot")
![Screenshot](https://github.com/koss822/misc/raw/master/imgs/heathcheck/healthcheck5.PNG "Route53 HealthCheckReboot screenshot")
![Screenshot](https://github.com/koss822/misc/raw/master/imgs/heathcheck/healthcheck6.PNG "Route53 HealthCheckReboot screenshot")
![Screenshot](https://github.com/koss822/misc/raw/master/imgs/heathcheck/healthcheck7.PNG "Route53 HealthCheckReboot screenshot")
![Screenshot](https://github.com/koss822/misc/raw/master/imgs/heathcheck/healthcheck8.PNG "Route53 HealthCheckReboot screenshot")
