#!/usr/bin/python2

### BEGIN INIT INFO
# Provides:     rpi-init
# Required-Start:   $remote_fs $syslog
# Required-Stop:    $remote_fs $syslog
# Default-Start:    2 3 4 5
# Default-Stop:
# Short-Description:    Raspberry Pi 3G Backup
### END INIT INFO

#
# Before running install neccesary modules!
# pip install -r requirements.txt

import sys, ConfigParser, os
from daemon import daemon
from rpicontrol import rcontrol

myconf = os.path.dirname(os.path.realpath(__file__))+'/rpi.ini'
 
class MyDaemon(daemon):
    def __init__(self, pidfile):
      daemon.__init__(self,pidfile)    
      self.rc = rcontrol(myconf)  

    def run(self):
      self.rc.run()
            
    def status(self):
      self.rc.status()
      
    def bkpstop(self):
      self.rc.stop()  
 
if __name__ == "__main__":
    config = ConfigParser.RawConfigParser()
    config.read(myconf)
    testing = config.getboolean('global', 'testing')
    daemon = MyDaemon(config.get('global', 'pidfile'))
    rc = rcontrol(myconf)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            if testing:
                rc.run()
            else:
                daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.bkpstop()
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.bkpstop()
            daemon.restart()
        elif 'status' == sys.argv[1]:
            if testing:
                rc.status()
            else:
                daemon.status()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart|status" % sys.argv[0])
        sys.exit(2)
