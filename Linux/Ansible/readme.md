# My Ansible scripts

## SMTP

This scripts enable you to use for example one GMail account for all outcoming SMTP e-mail from server using postfix. It also sends all mail destined to root mailbox to your email. It is very usefull when you have server and have some programs which uses e.g. mail command to send outgoing email. It rewrites FROM address (neccesary if you use foreign SMTP server for just one email mailbox) and destine email to foreign SMTP server.

### Set-up

Edit these files

```
hosts
```
Under myhosts edit servername which must be reachable using ssh under actual user

```
host_vars/server
```
rename this file to name of your server hostname and edit it's values to correct SMTP settings

### Run / Install
```
sudo pip3 install ansible
ansible-playbook smtp.yml
```
