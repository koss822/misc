#!/usr/bin/python3
import sys
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT = 5
DEBUG = False

if DEBUG:
    CHROME_DRIVER_PATH=""
    CFG_FNAME = ""
else:
    CHROME_DRIVER_PATH="/bin/chromedriver"
    CFG_FNAME = "/app/watch.json"

class Browser:
    def __enter__(self):
        options = webdriver.ChromeOptions()

        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu-sandbox')
        options.add_argument("--single-process")
        options.add_argument('window-size=1920x1080')
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36")
        if not DEBUG:
            options.binary_location = "/usr/bin/google-chrome"
        self.browser = webdriver.Chrome(
            executable_path=CHROME_DRIVER_PATH, options=options)
        return self.browser

    def __exit__(self, type, value, traceback):
        self.browser.quit()

def get_config(fname):
    with open(fname) as data:
        return json.load(data)

def get_element(by, txt):
    element_present = EC.presence_of_element_located((by, txt))
    WebDriverWait(browser, TIMEOUT).until(element_present)
    return browser.find_element(by, txt)

def accept_cookies():
    browser.get('https://finance.yahoo.com/')
    elem = get_element(By.NAME, 'agree')  # Find the search box
    elem.click()

def get_stock(stock) -> float:
    browser.get('https://finance.yahoo.com/')
    elem = get_element(By.NAME, 'yfin-usr-qry')  # Find the search box
    elem.send_keys(stock + Keys.RETURN)
    css_locator = 'span[data-reactid="32"]'
    return float(get_element(By.CSS_SELECTOR, css_locator).text)

def get_currency(curr):
    css_locator = 'span[data-reactid="32"]'
    browser.get(f'https://finance.yahoo.com/quote/{curr}=x/')
    return float(get_element(By.CSS_SELECTOR, css_locator).text)

with Browser() as browser:
    accept_cookies()
    total = 0
    print("="*80)
    for stock in get_config(CFG_FNAME).get('stocks'):
        stockprice = get_stock(stock.get('symbol'))
        currency = get_currency(stock.get('currency'))
        count = stock.get('count')
        name = stock.get('name')
        total_per_stock = stockprice * currency * count
        total += total_per_stock
        print(f"Stock {name} costs {stockprice} per share, with {count} shares totalling {total_per_stock}")
    print("="*80)
    print(f"Total price of stocks is {total}")
    print("="*80)
