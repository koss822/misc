#!/usr/bin/env python3
# apt install easy-rsa
import yaml,os

curdir = os.path.dirname(os.path.abspath(__file__)) + '/'
stream = open("vpn.yml", "r")
config = list(yaml.load_all(stream))[0]
vpns = config['clients']
skmain = curdir + 'server'
skdir = skmain + '/keys'
cafile = skdir + '/ca.key'
dirs = ['server', 'clients', 'server/ccd', 'server/keys', 'tmp']

print('======== OpenVPN Config Generator =========')

# create initial directories
for mydir in dirs:
    try:
        os.mkdir(curdir + mydir)
    except:
        pass

def createconfig(vpn):
    return """client
dev tun
proto udp
remote """ + config['server']['fqdn'] + """
port """ + config['server']['port'] + """
persist-key
persist-tun
ca keys/ca.crt
cert keys/""" + vpn['name'] + """.crt
key keys/""" + vpn['name'] + """.key
comp-lzo
cipher AES-256-CBC
remote-cert-eku "TLS Web Server Authentication"
"""

def createccd(vpn):
    ccdtext = "ifconfig-push " + vpn['ip'] + " " + vpn['subnet'] + "\n"
    ccdname = skmain + '/ccd/' + vpn['name']
    ccdfile = open(ccdname, "w")
    ccdfile.write(ccdtext)
    ccdfile.close()

# generate ca
if not os.path.isfile(cafile):
    print("CA authority is non existent, installing...")
    os.system("""cp -R /usr/share/easy-rsa tmp/ &&
            cd tmp/easy-rsa &&
            ln -s openssl-1.0.0.cnf openssl.cnf &&
            . ./vars &&
            ./clean-all &&
            ./build-ca --batch &&
            cd ../.. && 
            cp tmp/easy-rsa/keys/ca.* server/keys/""")

# generate server key
serverkey = skdir + '/server.key'
if not os.path.isfile(serverkey):
    os.system("""cd tmp/easy-rsa &&
    . ./vars &&
    ./build-key-server --batch server &&
    cd ../.. &&
    cp tmp/easy-rsa/keys/server.* server/keys/""")

# generate client vpns
for vpn in vpns:
    vpndir = curdir + '/clients/' + vpn['name']
    vpnconfig = vpndir + '/' + vpn['name'] + '.client.conf'
    if not os.path.isfile(vpnconfig):
        try:
            print("Adding VPN [ " + vpn['name'] + " ]")
            os.mkdir(vpndir)
            os.mkdir(vpndir + '/keys')
            vpnc_file = open(vpnconfig, "w")
            vpnc_file.write(createconfig(vpn))
            vpnc_file.close()
            createccd(vpn)
        except:
            pass
        os.system("""cd tmp/easy-rsa &&
        . ./vars &&
        ./build-key --batch """ + vpn['name'] + """ &&
        cd ../.. &&
        cp tmp/easy-rsa/keys/""" + vpn['name'] + ".* " + vpndir + """/keys/ &&
        cp server/keys/ca.crt """ + vpndir + "/keys/")

# generate server config
serverconf = "port " + config['server']['port'] + """
proto """ + config['server']['proto'] + """
dev tun
ca keys/ca.crt
cert keys/server.crt
key keys/server.key
dh keys/dh2048.pem
comp-lzo
cipher AES-256-CBC
log /var/log/openvpn.log
keepalive 10 120
server """ + config['server']['topology'] + """
topology subnet
client-config-dir ccd
"""
serverc = skmain + '/server.conf'
serverc_file = open(serverc, "w")
serverc_file.write(serverconf)
serverc_file.close()

# generate DH
if not os.path.isfile(skdir + '/dh2048.pem'):
    os.system("""cd tmp/easy-rsa &&
        . ./vars &&
        ./build-dh &&
        cd ../.. &&
        cp tmp/easy-rsa/keys/dh2048.pem """ + skdir)


print('======== Done =========')
