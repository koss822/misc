#!/usr/bin/python3
#################################################################################
# SSH Tunneller wrapper script 1.0
# Author: Martin Konicek (m.konicek@t-mobile.cz)
#################################################################################
import yaml, pickle, subprocess, os, signal, sys, random

#################################################################################
# Defaults
#################################################################################

mainconf = '/usr/local/sshtunnel-app/settings/sshtunnel.yml'
pidconf = '/usr/local/sshtunnel-app/ssh.pid' # it should be removed on every machine boot
autossh = '/usr/bin/autossh'

#################################################################################
# Main functions
#################################################################################

def load_config(config):
    with open(config, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def getcmd(tunnel):
    monport = random.randint(100,999)
    cmd = "{} -4 -oStrictHostKeyChecking=no -i /usr/local/sshtunnel-app/settings/id_rsa -M 60{} -N".format(autossh, monport)
    for port in tunnel['ports']:
        cmd += " -L {}:{}:{}:{}".format(myconf['main']['listen'], port['local'], port['remote_target'], port['remote_port'])
    cmd += " {}".format(tunnel['remote'])
    return cmd

def managepid(append = None): # Always returns all running pids, you can append pid by using append parameter
    try:
        pids = pickle.load(open(pidconf, 'rb')) # deserialize
    except: # if pidconf not exist
        pids = list()
    
    if append is not None:
        pids.append(append)

    pickle.dump(pids, open(pidconf, 'wb')) # serialize
    return pids

def runcmd(cmd):
    p = subprocess.Popen(cmd.split(' '), env=my_env)
    print("Starting PID: %s" % p.pid)
    print("CMD: %s" % cmd)
    managepid(p.pid)

#################################################################################
# Main code
#################################################################################
my_env = os.environ.copy()
my_env["AUTOSSH_LOGFILE"] = "/var/log/autossh.log"

myconf = load_config(mainconf)
for tunnel in myconf['tunnels']:
    runcmd(getcmd(tunnel))

os.system("tail -f /var/log/autossh.log")
