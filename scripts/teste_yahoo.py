import yfinance as yf

ticker = yf.Ticker("MXRF11.SA")

print(ticker.history(period="5d"))