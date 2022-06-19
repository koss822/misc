# Python, Selenium and Firefox Docker image

## Intro
If you do not want to compile you can use

```
docker pull krab55/selenium-firefox:0.5
```

## Running
### Docker compose file
```
ChangeItToYourCrawlerName:
  image: docker.io/krab55/selenium-firefox:0.5
  restart: always
  container_name: ChangeItToYourCrawlerName
  volumes:
    - "/home/user/docker/app:/opt/app"
    - "/home/user/.aws:/.aws"
```

* Mount app directory to /opt/app
* It should contains main.py file for crawler
* Optionally you can mount your AWS credentials and connect to AWS services (e.g. AWS SNS for sending alerts)