FROM ubuntu:bionic
RUN apt update
RUN apt install -y python3 python3-yaml autossh
RUN touch /var/log/autossh.log
ADD sshtunnel-app /usr/local/sshtunnel-app
ENTRYPOINT /usr/local/sshtunnel-app/sshtunnel.py
