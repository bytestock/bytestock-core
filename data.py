"""Libraries"""
import yfinance as yf
import streamlit as st
import os
import time
import json
from misc import Misc
import datetime

class Data:
    def __init__(self,stocks, days) -> None:
        self.ticks = int(time.time())
        self.miscellaneous = Misc(self.ticks, "", "", "")
        self.ticker = stocks
        self.days = days

    def getOCHLData(self) ->list:
        """Gets Data"""
        now = datetime.datetime.now()
        d = datetime.timedelta(days = self.days)
        start = now - d
        start = start.strftime('%Y-%m-%d')

        rate_limit_free = self.miscellaneous.telemetry()
        if rate_limit_free:
            stock = yf.Ticker(self.ticker)
            data = yf.download(self.ticker, start=start, end=now.strftime('%Y-%m-%d'))
        
        #open_days, closed_days = misc.wasMarketClosedFrom(ticks - start, ticks, days-1)
        open_days = data.index.tolist()
        daily_close = list(data['Close'])
        daily_adj_close = list(data['Adj Close'])
        daily_open = list(data['Open'])
        daily_high = list(data['High'])
        daily_low = list(data['Low'])

        return open_days, daily_open, daily_close, daily_adj_close, daily_high, daily_low
    
    @st.cache_data
    def getRealTimeOCHL(self) ->list:
        """Gets Real Time Data"""
        rate_limit_free = self.miscellaneous.telemetry()
        if rate_limit_free:
            stock = yf.Ticker(self.ticker)
            data = stock.fast_info
        
        rt_previous_close = list(stock.history(period=f'2d')['Close'])[-2]
        rt_open = data.open
        rt_current = data.last_price
        rt_high = data.day_high
        rt_low = data.day_low
        rt_change = rt_current - data.previous_close
        rt_change_percent = round((rt_current - rt_previous_close)/((rt_current + rt_previous_close) / 2) * 100, 2)

        return rt_previous_close, rt_open, rt_current, rt_high, rt_low, rt_change, rt_change_percent

