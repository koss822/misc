#!/usr/bin/python2
# https://github.com/dbader/schedule
import os, time, pyjsonrpc, collections, schedule, threading, ConfigParser
import smtplib, syslog, time

class rcontrol():  
  def __init__(self, myconf):
    config = ConfigParser.RawConfigParser()
    config.read(myconf)
    self.port = config.getint('global', 'port')
    self.listen = config.get('global', 'listen')
    self.http_client = pyjsonrpc.HttpClient("http://localhost:%s" % 
        self.port)
    Pinger.cmdup = config.get('global', 'cmdup')
    Pinger.cmddown = config.get('global', 'cmddown')
    Pinger.checkip = config.get('global', 'checkip')
    testing = config.getboolean('global', 'testing')
    if testing:
      Pinger.pstats = collections.deque([1], 1) # just one ping for testing
    Pinger.mailer = Mailer(myconf)
    
  # Actually run daemon
  def run(self):
    cwatch = ConnWatch()
    syslog.syslog('NETBKP: Service started')
    http_server = pyjsonrpc.ThreadingHttpServer(
      server_address = (self.listen, self.port),
      RequestHandlerClass = RequestHandler
    )
    http_server.serve_forever()
    
  # Use JSON RPC to get status of daemon
  def status(self):
    try:
      print(self.http_client.pingstatus())
    except:
      print("Daemon is probably down")
      
  def stop(self):
    if Pinger.backup == True:
      Pinger.disable_backup()
    syslog.syslog('NETBKP: Service stopped')
     
# Pinger - everything is static for a reason     
class Pinger():
  backup = False
  pstats = collections.deque(5*[1], 5)
  checkip = "127.0.0.1"
  cmdup = ""
  cmddown = ""
  lastchange = 0
  flapmsg = False
  
  @staticmethod
  def getpingsum():
    mysum = 0
    for one in Pinger.pstats:
        mysum += one
    return mysum
  
  @staticmethod
  def ping():
    response = os.system("ping -c 1 %s" % Pinger.checkip)
    if response == 0: # Success, exit code 0
      Pinger.pstats.append(1)
    else:
      Pinger.pstats.append(0)

    if Pinger.getpingsum() == 0 and Pinger.backup == False:
        # Could not reach cable net and not using backup  
        Pinger.switch_to_backup()
    if Pinger.getpingsum() == 1 and Pinger.backup == True:
        # Prevent flapping, might change state only once per hour
        if (Pinger.lastchange > 0) and ((time.time()-Pinger.lastchange) < 3600): # 3600 seconds -> 1 hour 
          if not Pinger.flapmsg:
            syslog.syslog('NETBKP: flapping detected')
            Pinger.flapmsg = True
        else:
          Pinger.flapmsg = False
          Pinger.lastchange = time.time() # e.g. 464864.25948 seconds
          # Could reach cable net and backup is in use
          Pinger.disable_backup()
        
  @staticmethod  
  def switch_to_backup():
    Pinger.backup = True
    syslog.syslog('NETBKP: Switching to backup connection')
    os.system(Pinger.cmdup)
    time.sleep(10) # wait until we dial 3g connection
    try:
      Pinger.mailer.sendnotification(Pinger.backup)
    except:
      syslog.syslog('NETBKP: Unable to send notification e-mail')
  
  @staticmethod
  def disable_backup():
    Pinger.backup = False
    syslog.syslog('NETBKP: Switching to primary connection')
    try:
      Pinger.mailer.sendnotification(Pinger.backup)
    except:
      syslog.syslog('NETBKP: Unable to send notification e-mail')
    os.system(Pinger.cmddown)

# Class for pinging every minute
class ConnWatch():
  def __init__(self):
    schedule.every().minute.do(Pinger.ping)
    self.run_continuously()
    
  def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """
    cease_continuous_run = threading.Event()
  
    class ScheduleThread(threading.Thread):
      @classmethod
      def run(cls):
        while not cease_continuous_run.is_set():
          schedule.run_pending()
          time.sleep(interval)
  
    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run
    
# JSON RPC Server to check daemon status
class RequestHandler(pyjsonrpc.HttpRequestHandler):
  
  @pyjsonrpc.rpcmethod      
  def pingstatus(self):
    if Pinger.backup:
      state = 'active'
    else:
      state = 'inactive'
    out = ("Backup status is %s\n" % state)
    out += ("Last %s/5 pings were succesfull" % Pinger.getpingsum())
    return out
    
# Class for sending outgoing mails
class Mailer(): 
  def __init__(self, myconf):
    config = ConfigParser.RawConfigParser()
    config.read(myconf)
    self.to = config.get('mail', 'to')
    self.smtpuser = config.get('mail', 'smtpuser')
    self.smtppass = config.get('mail', 'smtppass')
    self.smtpserver = config.get('mail', 'smtpserver')
    self.subject = config.get('mail', 'subject')
    self.tlsport = config.getint('mail', 'tlsport')
    self.up = config.get('mail', 'up')
    self.down = config.get('mail', 'down')
  
  def sendnotification(self, bkpactive):
    smtpserver = smtplib.SMTP(self.smtpserver,self.tlsport)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(self.smtpuser, self.smtppass)
    header = 'To:' + self.to + '\n' + 'From: '
    header += self.smtpuser + '\n' + ('Subject:%s \n' % self.subject)
    msg = header + '\n'
    if bkpactive:
      msg += self.up
    else:
      msg += self.down
    msg += '\n\n'
    smtpserver.sendmail(self.smtpuser, self.to, msg)
    smtpserver.close()