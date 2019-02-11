# TightVNC on Lubuntu 18.04

![TightVNC screenshot](https://raw.githubusercontent.com/koss822/misc/master/imgs/tightvnc.jpg "TightVNC Screenshot")

## Basic info
This is my small set-up how to run LXDE on Lubuntu, Xubuntu or any other Ubuntu distro with LXDE installed in TightVNC as daemon under your user.

Let's pretend that you are an user peter and you login to your machine, here is the tutorial

## Installation

1. Install lxde and tightvnc under Ubuntu
'''
peter@server$ apt install lxde tightvncserver
'''
2. Run and kill tightvnc
'''
peter@server$ tightvncserver
Starting server on :1
peter@server$ tightvncserver -kill :1
'''
3. Copy xstartup to .vnc and make it executable
'''
peter@server$ cp ~/misc/.../xstartup ~/.vnc/
peter@server$ chmod +x ~/.vnc/xstartup
'''
4. Try to run tightvncserver
'''
peter@server$ tightvncserver :10 -geometry 1152x864

New 'X' desktop is server:10
'''
5. Try to connect to server:5910 with TightVNC client
6. If it won't work examine
'''
less /home/peter/.vnc/server:10.log
'''
7. Kill TightVNC server
'''
tightvncserver -kill :10
'''
8. Install TightVNC service
'''
cp ~/misc/.../tightvnc.service /etc/systemd/system/tightvnc.service
vi /etc/systemd/system/tightvnc.service (modify username)
systemctl start tightvnc
systemctl enable tightvnc
'''
9. Enjoy
