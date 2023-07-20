import yfinance as yf
from flask import Flask
from cachetools import TTLCache
import datetime

app = Flask(__name__)
cache = TTLCache(maxsize=100, ttl=datetime.timedelta(hours=6), timer=datetime.datetime.now)

@app.route('/')
def fetch_sp500_price():
    # Fetch the data for the S&P 500 index
    if 'sp500_price' in cache:
        result = cache['sp500_price']
        print("Retrieving cached result for sp500_price")
    else:
        # Perform the computation
        result = f"Result for sp500_price"
        print("Performing computation for sp500_price")

        sp500 = yf.Ticker('SPY')
        history = sp500.history(period='1d')
        sp500_price = history['Close'][-1]
        
        # Store the result in the cache
        cache['sp500_price'] = sp500_price

    return f"stock_price{{stock=\"sp500\"}} {cache['sp500_price']}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)