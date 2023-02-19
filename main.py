import yfinance as yf

goog = yf.Ticker("GOOG")
goog.fast_info


data = goog.history(period="1mo")
#shares = msft.get_shares_full(start = "2022-01-01", end = None)

print(data)
