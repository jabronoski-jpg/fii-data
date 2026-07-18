import yfinance as yf


ticker = yf.Ticker(
    "MXRF11.SA"
)


dividendos = ticker.dividends


print(dividendos)