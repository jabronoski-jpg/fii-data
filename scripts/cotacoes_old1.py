import json
from datetime import datetime
from pathlib import Path

import yfinance as yf

import config
import logger


def carregar_tickers():

    with open(
        config.FIIS_JSON,
        "r",
        encoding="utf-8"
    ) as arquivo:

        dados = json.load(arquivo)

    tickers = []

    for fii in dados["dados"]:
        tickers.append(
            fii["ticker"] + ".SA"
        )

    return tickers



def buscar_cotacoes(tickers):

    logger.info(
        f"Consultando {len(tickers)} ativos no Yahoo..."
    )

    resultado = {}

    dados = yf.download(
        tickers,
        period="7d",
        progress=False,
        group_by="ticker",
        auto_adjust=False
    )


    for ticker in tickers:

        try:

            fechamento = (
                dados[ticker]["Close"]
                .dropna()
                .iloc[-1]
            )

            codigo = ticker.replace(".SA", "")

            resultado[codigo] = {
                "preco": round(
                    float(fechamento),
                    2
                )
            }


        except Exception as erro:

            logger.aviso(
                f"Falha {ticker}: {erro}"
            )


    return resultado



def salvar(resultado):

    arquivo = (
        config.COTACOES_JSON
    )


    saida = {

        "versao": 1,

        "gerado_em":
            datetime.utcnow()
            .strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),

        "origem":
            "Yahoo Finance",

        "quantidade":
            len(resultado),

        "dados":
            resultado
    }


    with open(
        arquivo,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            saida,
            f,
            indent=4,
            ensure_ascii=False
        )


    logger.info(
        f"Cotações salvas: {len(resultado)}"
    )

    logger.info(
        f"Arquivo: {arquivo}"
    )



def executar():

    logger.linha()

    logger.info(
        "Lendo FIIs..."
    )

    tickers = carregar_tickers()


    logger.info(
        f"Tickers encontrados: {len(tickers)}"
    )


    cotacoes = buscar_cotacoes(
        tickers
    )


    salvar(
        cotacoes
    )

    logger.linha()



if __name__ == "__main__":

    executar()