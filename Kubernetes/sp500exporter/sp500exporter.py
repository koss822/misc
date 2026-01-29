import yfinance as yf
from flask import Flask
from cachetools import TTLCache
import datetime

app = Flask(__name__)
cache = TTLCache(maxsize=100, ttl=datetime.timedelta(hours=6), timer=datetime.datetime.now)

@app.route('/metrics')
def fetch_sp500_price():
    if 'sp500_price' in cache and cache['sp500_price'] is not None:
        print("Retrieving cached result for sp500_price")
        return f'stock_price{{stock="sp500"}} {cache["sp500_price"]}'
    
    print("Performing computation for sp500_price")
    sp500 = yf.Ticker('SPY')
    history = sp500.history(period='5d')  # Use 5d for reliability
    
    if history.empty:
        print("No SPY data available")
        return f'stock_price{{stock="sp500"}} NaN'  # Graceful fallback
    
    sp500_price = history['Close'].iloc[-1]  # Positional iloc[-1]
    cache['sp500_price'] = float(sp500_price)  # Ensure numeric
    
    return f'stock_price{{stock="sp500"}} {cache["sp500_price"]}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)