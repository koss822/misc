# SMTP test sender in python

if you are sending from local networks to solution using ansible above please configure mynetworks in postfix

## vi /etc/postfix/main.cf

```
mynetworks = ... 192.168.0.0/16 10.0.0.0/8
```
## restart postfix
```
sudo systemctl restart postfix
```