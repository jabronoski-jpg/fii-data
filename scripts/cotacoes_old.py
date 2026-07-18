import json

from config import FIIS_JSON
from logger import info, finalizar


def carregar_tickers():

    with open(
        FIIS_JSON,
        "r",
        encoding="utf-8"
    ) as f:

        dados = json.load(f)

    tickers = []

    for fii in dados["dados"]:

        codigo = fii["codigo"].strip().upper()

        tickers.append(
            codigo + "11.SA"
        )

    return tickers


def main():

    info("Lendo fiis.json...")

    tickers = carregar_tickers()

    info(
        f"{len(tickers)} tickers encontrados."
    )

    print()

    print("Primeiros 10:")

    for ticker in tickers[:10]:

        print(ticker)

    finalizar()


if __name__ == "__main__":

    main()