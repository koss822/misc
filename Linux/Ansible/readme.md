# My Ansible scripts

## SMTP Relay which changes FROM field and Send system mails using GMail or other freemail account

### Diagram
![SMTP Relay](https://github.com/koss822/misc/raw/master/imgs/smtprelay.png "SMTP Relay diagram")

### What it does?

* Receive e-mail on localhost of your machine (you can use standard mail account or send it to root@yourmachine alias)
* Modify FROM header of your mail and change it to predefined text (e.g. Gmail allow sending e-mails only with FROM header which matches account e-mail)
* Connect to Gmail or any other freemail account using SSL encrypted SMTP
* Send e-mail to specified address (in case you are using root@yourmachine alias it sends e-mail to predefined machines

### Example usage

* You need to send e-mails from your PHP scripts but do not won't to configure your own SMTP server
* You need to send system e-mails (e.g. cron reports)

### Description

This scripts enable you to use for example one GMail account for all outcoming SMTP e-mail from server using postfix. It also sends all mail destined to root mailbox to your email. It is very usefull when you have server and have some programs which uses e.g. mail command to send outgoing email. It rewrites FROM address (neccesary if you use foreign SMTP server for just one email mailbox) and destine email to foreign SMTP server.

### Run / Install
1. Edit this file, and insert details of your Gmail or other e-mail account
```
host_vars/localhost
```
2. Install ansible and run playbook
```
sudo pip3 install ansible
ansible-playbook smtp.yml
```

### Asciinema tutorial on clean Ubuntu 18.04 machine
[![asciicast](https://asciinema.org/a/229978.svg)](https://asciinema.org/a/229978)
