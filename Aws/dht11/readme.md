# Temperature monitoring for AWS
## Screenshot
![Screenshot](https://github.com/koss822/misc/blob/master/imgs/aws-dht11.png?raw=true "DHT11 Cloudwatch screenshot")

## Diagram
![Diagram](https://github.com/koss822/misc/blob/master/imgs/dht11.png?raw=true "DHT11 Cloudwatch diagram")

## Information
DHT11 utilities for Raspberry Pi works very straigtforward. At first you connect DHT11 sensor to RaspberryPi and edit /etc/temp.yaml (you need to modify PIN where you connected VOut of your DHT11 sensor).

After that you install utilities on your RaspberryPi and also modify AWS API KeyPair which you firstly create in AWS IAM with ability to put Cloudwatch events and metrics.

Then you are ready. Once you start a "temp" service you it will upload your metric to AWS Cloudwatch. Also on each measurement there will be uploaded logs about success or failure. I strongly recommend to create a Cloudwatch alarm which watch keyword "success" in logs and if there are less than 1 success per hour I would recommend sending an alert to your e-mail address to inform you that there are errors in measurement (e.g. sensor or raspberry pi is broken).

## Installation
```
sudo -s
apt install python3-pip
pip3 install -r requirements.txt
cp temp.yaml /etc
vi /etc/temp.yaml
cp temp.service /etc/systemd/system/
cp temp.py /usr/local/bin/
systemctl daemon-reload
systemctl start temp
systemctl status temp
```
