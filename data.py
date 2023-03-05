import finnhub
import os
from dotenv import load_dotenv
import time
import json
import misc

load_dotenv()

API_KEY=os.getenv('API_KEY')
finnhub_client = finnhub.Client(api_key=API_KEY)

ticks = int(time.time())

def getOCHLData(ticker, days):
    start = days * 24 * 60 * 60

    rate_limit_free = misc.telemetry(ticker, days)
    if rate_limit_free:
        data = finnhub_client.stock_candles(ticker, 'D', ticks - start, ticks)

    open_days, closed_days = misc.wasMarketClosedFrom(ticks - start, ticks)
    daily_close = data.get('c')
    daily_open = data.get('o')
    daily_high = data.get('h')
    daily_low = data.get('l')

    return open_days, daily_open, daily_close, daily_high, daily_low

def getRealTimeOCHL(ticker):
    data = finnhub_client.quote(ticker)

    rt_open = data.get('o')
    rt_current = data.get('c')
    rt_high = data.get('h')
    rt_low = data.get('l')
    rt_change = data.get('d')
    rt_change_percent = data.get('dp')

    return rt_open, rt_current, rt_high, rt_low, rt_change, rt_change_percent