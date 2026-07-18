import json
from datetime import datetime, timezone

import yfinance as yf

import config
import logger



def carregar_fiis():

    with open(
        config.FIIS_JSON,
        "r",
        encoding="utf-8"
    ) as arquivo:

        dados = json.load(arquivo)


    return [
        fii["ticker"]
        for fii in dados["dados"]
    ]



def buscar_dividendos(ticker):

    simbolo = ticker + ".SA"


    try:

        ativo = yf.Ticker(
            simbolo
        )


        dividendos = ativo.dividends


        if dividendos.empty:

            return []


        lista = []


        for data, valor in dividendos.items():

            lista.append(
                {
                    "data":
                        data.strftime(
                            "%Y-%m-%d"
                        ),

                    "valor":
                        round(
                            float(valor),
                            6
                        )
                }
            )


        return lista


    except Exception as erro:

        logger.aviso(
            f"{ticker}: {erro}"
        )

        return []



def gerar_dividendos():

    tickers = carregar_fiis()


    resultado = {}

    sucesso = 0


    for i, ticker in enumerate(tickers, 1):

        logger.info(
            f"{i}/{len(tickers)} {ticker}"
        )


        dados = buscar_dividendos(
            ticker
        )


        if dados:

            resultado[ticker] = dados

            sucesso += 1



    saida = {

        "versao": 1,

        "gerado_em":
            datetime.now(
                timezone.utc
            ).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),

        "origem":
            "Yahoo Finance",

        "estatisticas": {

            "consultados":
                len(tickers),

            "com_dividendos":
                sucesso
        },

        "dados":
            resultado

    }


    with open(
        config.DIVIDENDOS_JSON,
        "w",
        encoding="utf-8"
    ) as arquivo:


        json.dump(
            saida,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


    logger.info(
        f"FIIs com dividendos: {sucesso}"
    )



if __name__ == "__main__":

    logger.linha()

    gerar_dividendos()

    logger.linha()