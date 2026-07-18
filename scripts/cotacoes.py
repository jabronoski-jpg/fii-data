import json
import warnings
from datetime import datetime

import yfinance as yf

import config
import logger


# Remove avisos desnecessários do yfinance/pandas
warnings.filterwarnings("ignore")


def carregar_fiis():

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
        f"Consultando {len(tickers)} ativos no Yahoo Finance..."
    )

    cotacoes = {}
    falhas = []

    dados = yf.download(
        tickers,
        period="7d",
        progress=False,
        group_by="ticker",
        auto_adjust=False,
        threads=True
    )


    for ticker in tickers:

        codigo = ticker.replace(
            ".SA",
            ""
        )

        try:

            serie = (
                dados[ticker]["Close"]
                .dropna()
            )


            if len(serie) == 0:

                raise Exception(
                    "Sem dados"
                )


            ultimo = serie.iloc[-1]


            cotacoes[codigo] = {

                "preco":
                    round(
                        float(ultimo),
                        2
                    )
            }


        except Exception:

            falhas.append(
                {
                    "ticker": codigo,
                    "motivo":
                        "Sem dados no Yahoo Finance"
                }
            )


    return cotacoes, falhas



def salvar(
    cotacoes,
    falhas,
    total
):

    data_pregao = None


    if cotacoes:

        # pega a data da primeira cotação válida
        primeiro = next(
            iter(cotacoes)
        )

        ticker = primeiro + ".SA"

        historico = yf.download(
            ticker,
            period="7d",
            progress=False,
            auto_adjust=False
        )


        if not historico.empty:

            data_pregao = (
                historico.index[-1]
                .strftime("%Y-%m-%d")
            )



    resultado = {

        "versao": 1,

        "gerado_em":
            datetime.utcnow()
            .strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),

        "origem":
            "Yahoo Finance",

        "data_pregao":
            data_pregao,


        "estatisticas": {

            "consultados":
                total,

            "com_cotacao":
                len(cotacoes),

            "sem_cotacao":
                len(falhas)
        },


        "dados":
            cotacoes,


        "falhas":
            falhas
    }



    with open(
        config.COTACOES_JSON,
        "w",
        encoding="utf-8"
    ) as arquivo:


        json.dump(
            resultado,
            arquivo,
            indent=4,
            ensure_ascii=False
        )



def executar():

    logger.linha()


    logger.info(
        "Lendo fiis.json..."
    )


    tickers = carregar_fiis()


    logger.info(
        f"Tickers encontrados: {len(tickers)}"
    )


    cotacoes, falhas = buscar_cotacoes(
        tickers
    )


    salvar(
        cotacoes,
        falhas,
        len(tickers)
    )


    logger.linha()


    logger.info(
        f"Cotações salvas: {len(cotacoes)}"
    )


    logger.info(
        f"Falhas: {len(falhas)}"
    )


    logger.linha()



if __name__ == "__main__":

    executar()