# Container with headless Firefox browser
#
# Much of the source comes from https://github.com/nathancahill/docker-firefox-headless
#
# docker build -t firefox-headless .
# docker run -it firefox-headless firefox -url http://example.com -p headless -no-remote -headless

FROM ubuntu:24.04

RUN  apt-get update \
    && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/*

# OPTIONAL: Install dumb-init (Very handy for easier signal handling of SIGINT/SIGTERM/SIGKILL etc.)
RUN wget https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_amd64.deb
RUN dpkg -i dumb-init_*.deb
ENTRYPOINT ["dumb-init"]

# Install Firefox
# In Debian, Firefox is called Iceweasel
ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
ARG FIREFOX_VERSION="latest"
RUN FIREFOX_DOWNLOAD_URL=$(if [ $FIREFOX_VERSION = "latest" ] || [ $FIREFOX_VERSION = "nightly-latest" ] || [ $FIREFOX_VERSION = "devedition-latest" ]; then echo "https://download.mozilla.org/?product=firefox-$FIREFOX_VERSION-ssl&os=linux64&lang=en-US"; else echo "https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2"; fi) \
    && apt-get update -qqy \
    && apt-get -qqy --no-install-recommends install iceweasel \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/* \
    && wget --no-verbose -O /tmp/firefox.tar.bz2 $FIREFOX_DOWNLOAD_URL \
    && apt-get -y purge iceweasel \
    && rm -rf /opt/firefox \
    && tar -C /opt -xjf /tmp/firefox.tar.bz2 \
    && rm /tmp/firefox.tar.bz2 \
    && mv /opt/firefox /opt/firefox-$FIREFOX_VERSION \
    && ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/bin/firefox

RUN ln -s /opt/firefox-$FIREFOX_VERSION /opt/firefox
RUN apt update
RUN apt install -y libxt6 python3 python3-pip
RUN firefox -CreateProfile "headless /moz-headless"  -headless
RUN pip3 install selenium boto3 webdriver-manager
RUN mkdir -p /opt/app
ENTRYPOINT ["/usr/bin/python3", "-u", "/opt/app/main.py"]