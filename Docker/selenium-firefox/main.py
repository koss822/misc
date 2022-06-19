import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import boto3
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
import os
from sys import platform


# Use your GITHUB token, it is needed for WebDriverManager to download the correct version of the driver
os.environ['GH_TOKEN'] = "ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# I develop on Windows, when platform is docker image I download credentials to AWS from there
# If you do not use AWS you do not need this code
if "linux" in platform:
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = "/.aws/credentials"
sns = boto3.client('sns', region_name="us-east-1")

# Initialize webdriver
options = webdriver.FirefoxOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_7) AppleWebKit/537.38 (KHTML, like Gecko) Chrome/75.0.3809.100 Safari/538.36")
options.add_argument("--headless")
browser = webdriver.Firefox(service=Service(
    GeckoDriverManager().install()), options=options)

# Here is your crawler code
browser.get("https://www.google.com/")
sleep(5)
browser.find_element_by_name("q").send_keys("selenium")

# Your Alert code
sns.publish(TopicArn="sns_topic_arn", Message="Alert: Selenium")
