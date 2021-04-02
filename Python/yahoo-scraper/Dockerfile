FROM centos:7

ADD repos /etc/yum.repos.d/
RUN yum install -y google-chrome-stable
RUN yum -y install python3-pip

ADD bin /bin/
RUN chmod 755 /bin/chromedriver

COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bin
RUN mkdir /app

ENTRYPOINT [ "/usr/bin/python3", "/app/scraper.py" ]