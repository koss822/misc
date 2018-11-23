#!/usr/bin/env python3
import os,time
def reachable():
    for i in range(0,3):
        time.sleep(60)
        if os.system('ping -c1 YOUR_VPN_SERVER_PRIVATE_IP 2>&1 > /dev/null') == 0:
            print('ping succesfull')
            return True
        print('host unreachable')
    return False



while(True):
    if reachable():
        continue
    print('restarting openvpn')
    os.system('systemctl restart openvpn@YOUR_CONFIG_NAME.service')
