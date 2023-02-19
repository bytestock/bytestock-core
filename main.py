import yfinance as yf
import os
from dotenv import load_dotenv

load_dotenv()

goog = yf.Ticker("GOOG")
goog.fast_info


data = goog.history(period="1y")
#shares = msft.get_shares_full(start = "2022-01-01", end = None)

print(data)
