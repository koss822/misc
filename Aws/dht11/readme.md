# Temperature monitoring for AWS

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
