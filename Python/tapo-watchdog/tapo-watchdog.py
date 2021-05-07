#!/usr/bin/python3
import json
import sys
import time

from PyP100 import PyP100
from pythonping import ping

CONFIG = "/etc/tapo-config.json"
with open(CONFIG) as config:
    cfg = json.load(config)


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def wait_time(minutes):
    for i in range(minutes):
        left = minutes-i
        print(f"{left} minutes left before resuming operation")
        time.sleep(60)


def p100_login():
    # Creating a P100 plug object
    p100 = PyP100.P100(cfg['SOCKET'], cfg['USER'], cfg['PASS'])
    p100.handshake()  # Creates the cookies required for further methods
    p100.login()  # Sends credentials to the plug and creates AES Key and IV for further methods
    return p100


def start():
    time.sleep(10)
    print("Powering ON...")
    p100 = p100_login()
    p100.turnOn()  # Sends the turn on request


def restart():
    print("Restarting 5G...")
    p100 = p100_login()
    p100.turnOff()  # Sends the turn off request
    time.sleep(5)
    p100.turnOn()  # Sends the turn on request
    resume = False


sys.stdout = Unbuffered(sys.stdout)
resume = True
errors = 0

start()  # Make sure device is initially powered on

while True:
    try:
        time.sleep(10)
        print("pinging")
        response = ping(cfg['FQDN'], count=1)
        print(response)
        if "timed" in repr(response):
            errors += 1
            if errors > int(int(cfg['WAIT'])/10) and resume:
                restart()
                errors = 0
        else:
            errors = 0
            resume = True
    except Exception as ex:
        print(f"EXCEPTION: {repr(ex)}")
