import finnhub
import os
from dotenv import load_dotenv
import time
import json

load_dotenv()

API_KEY=os.getenv('API_KEY')
finnhub_client = finnhub.Client(api_key=API_KEY)

ticks = int(time.time())

def getData(ticker):
    data = finnhub_client.stock_candles(ticker, 'D', ticks - 31556926, ticks)

    daily_close = data.get('c')
    daily_open = data.get('o')
    daily_high = data.get('h')
    daily_low = data.get('l')

    return daily_open, daily_close, daily_high, daily_low
