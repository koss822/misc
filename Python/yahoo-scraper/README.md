# Yahoo finance scraper

Simple yahoo finance scraper to download financial data and convert them to currency you need (using Google Chrome and Docker)

## Diagram
![Screenshot](https://raw.githubusercontent.com/koss822/misc/master/imgs/yahoo-scraper-diagram.png "Yahoo scraper diagram")

## Installation
1. Download chromium (see readme in bin)
2. build and run, see below

```
docker build .
docker run -v C:/YOURPATH/yahoo-scrapper/app:/app YOURHASH
```