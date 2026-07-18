import yfinance as yf

tickers = [
    "MXRF11.SA",
    "HGLG11.SA",
    "XPLG11.SA",
    "KNRI11.SA",
    "VISC11.SA"
]

dados = yf.download(
    tickers=tickers,
    period="5d",
    progress=False,
    group_by="ticker",
    auto_adjust=False
)

print(dados)