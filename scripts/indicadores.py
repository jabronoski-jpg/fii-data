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



def carregar_cotacoes():

    dados = carregar_json(
        config.COTACOES_JSON
    )

    return dados["dados"]



def carregar_segmentos():

    dados = carregar_json(
        config.SEGMENTOS_JSON
    )

    return dados["classificacao"]



def carregar_dividendos():

    dados = carregar_json(
        config.DIVIDENDOS_JSON
    )

    return dados["dados"]



def calcular_dividendos_12m(historico):

    total = 0

    for item in historico:

        total += item["valor"]


    return round(
        total,
        6
    )



def gerar():

    logger.info(
        "Carregando dados..."
    )


    cotacoes = carregar_cotacoes()

    segmentos = carregar_segmentos()

    dividendos = carregar_dividendos()


    indicadores = {}


    for ticker, preco in cotacoes.items():


        registro = {

            "preco":
                preco["preco"],

            "tipo":
                None,

            "segmento":
                None,

            "ultimo_dividendo":
                0,

            "dividendos_12m":
                0,

            "dy_12m":
                0

        }


        if ticker in segmentos:

            registro["tipo"] = segmentos[ticker].get(
                "tipo"
            )

            registro["segmento"] = segmentos[ticker].get(
                "segmento"
            )


        if ticker in dividendos:


            historico = dividendos[ticker]


            if historico:


                registro["ultimo_dividendo"] = (
                    historico[-1]["valor"]
                )


                total = calcular_dividendos_12m(
                    historico[-12:]
                )


                registro["dividendos_12m"] = total


                if preco["preco"] > 0:

                    registro["dy_12m"] = round(
                        (total / preco["preco"]) * 100,
                        2
                    )


        indicadores[ticker] = registro



    saida = {

        "versao": 1,

        "gerado_em":
            datetime.now(
                timezone.utc
            ).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),

        "origem":
            "Calculado",

        "quantidade":
            len(indicadores),

        "dados":
            indicadores
    }



    with open(
        config.INDICADORES_JSON,
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
        f"Indicadores gerados: {len(indicadores)}"
    )



if __name__ == "__main__":

    logger.linha()

    gerar()

    logger.linha()