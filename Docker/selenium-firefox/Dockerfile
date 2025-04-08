# Container with headless Firefox browser
#
# Much of the source comes from https://github.com/nathancahill/docker-firefox-headless
#
# docker build -t firefox-headless .
# docker run -it firefox-headless firefox -url http://example.com -p headless -no-remote -headless

FROM ubuntu:24.04

RUN  apt-get update \
    && apt-get install -y wget ca-certificates netcat-openbsd xz-utils libgtk-3-0 \
    libdbus-glib-1-2 libx11-xcb1 libxt6 libxrender1 libxrandr2 libasound2t64 python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN update-ca-certificates

# OPTIONAL: Install dumb-init (Very handy for easier signal handling of SIGINT/SIGTERM/SIGKILL etc.)
RUN nc -zv objects.githubusercontent.com 443
RUN wget "https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_amd64.deb"
RUN dpkg -i dumb-init_*.deb
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# Install Firefox
# In Debian, Firefox is called Iceweasel
ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
ARG FIREFOX_VERSION="latest"
RUN FIREFOX_DOWNLOAD_URL=$(if [ $FIREFOX_VERSION = "latest" ] || [ $FIREFOX_VERSION = "nightly-latest" ] || [ $FIREFOX_VERSION = "devedition-latest" ]; then echo "https://download.mozilla.org/?product=firefox-$FIREFOX_VERSION-ssl&os=linux64&lang=en-US"; else echo "https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.xz"; fi) \
    && apt-get update -qqy \
    && apt-get -qqy --no-install-recommends install iceweasel \
#   && rm -rf /var/lib/apt/lists/* /var/cache/apt/* \
    && wget --no-verbose -O /tmp/firefox.tar.xz $FIREFOX_DOWNLOAD_URL \
    && apt-get -y purge iceweasel \
    && rm -rf /opt/firefox \
    && tar -C /opt -xJf /tmp/firefox.tar.xz \
    && rm /tmp/firefox.tar.xz \
    && mv /opt/firefox /opt/firefox-$FIREFOX_VERSION \
    && ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/bin/firefox

RUN ln -s /opt/firefox-$FIREFOX_VERSION /opt/firefox
RUN apt update
RUN apt install -y libxt6 python3 python3-pip
RUN firefox -CreateProfile "headless /moz-headless"  -headless
RUN mkdir -p /opt/app
WORKDIR /opt/app
RUN python3 -m venv venv
RUN . /opt/app/venv/bin/activate && pip3 install selenium boto3 webdriver-manager
COPY main.py /opt/app/main.py
CMD ["/opt/app/venv/bin/python", "-u", "/opt/app/main.py"]