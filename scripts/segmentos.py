import json
from datetime import datetime, timezone

import config
import logger


def carregar_json(arquivo):

    with open(
        arquivo,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def salvar_json(arquivo, dados):

    with open(
        arquivo,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            dados,
            f,
            indent=4,
            ensure_ascii=False
        )



def carregar_tickers_b3():

    dados = carregar_json(
        config.FIIS_JSON
    )

    return {
        fii["ticker"]
        for fii in dados["dados"]
    }



def gerar_segmentos():

    logger.info(
        "Lendo FIIs da B3..."
    )

    tickers_b3 = carregar_tickers_b3()


    logger.info(
        "Lendo classificação manual..."
    )

    classificacao = carregar_json(
        config.DOCS / "classificacao_fiis.json"
    )


    resultado = {}

    erros = []


    for ticker, dados in classificacao.items():


        if ticker not in tickers_b3:

            erros.append(
                ticker
            )

            continue


        resultado[ticker] = dados



    saida = {

        "versao": 1,

        "gerado_em":
            datetime.now(
        timezone.utc
        ).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),

        "quantidade":
            len(resultado),

        "classificacao":
            resultado
    }


    salvar_json(
        config.SEGMENTOS_JSON,
        saida
    )


    logger.info(
        f"Segmentos gerados: {len(resultado)}"
    )


    if erros:

        logger.aviso(
            f"FIIs não encontrados: {erros}"
        )



if __name__ == "__main__":

    logger.linha()

    gerar_segmentos()

    logger.linha()