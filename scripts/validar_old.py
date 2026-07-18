import json

import config
import logger


def carregar_json(arquivo):

    with open(
        arquivo,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def validar_duplicados(lista):

    duplicados = [
        item
        for item in set(lista)
        if lista.count(item) > 1
    ]

    return duplicados



def carregar_fiis():

    dados = carregar_json(
        config.FIIS_JSON
    )

    tickers = [
        fii["ticker"]
        for fii in dados["dados"]
    ]

    return tickers



def validar_cotacoes(tickers_b3):

    dados = carregar_json(
        config.COTACOES_JSON
    )

    cotacoes = dados["dados"]

    erros = []

    for ticker in cotacoes:

        if ticker not in tickers_b3:

            erros.append(
                ticker
            )

    return (
        len(cotacoes),
        erros
    )



def validar_segmentos(tickers_b3):

    dados = carregar_json(
        config.SEGMENTOS_JSON
    )

    classificacao = dados["classificacao"]

    erros = []

    for ticker in classificacao:

        if ticker not in tickers_b3:

            erros.append(
                ticker
            )

    return (
        len(classificacao),
        erros
    )



def executar():

    logger.linha()

    logger.info(
        "Validando base de FIIs..."
    )


    tickers = carregar_fiis()


    duplicados = validar_duplicados(
        tickers
    )


    cotacoes, erros_cotacoes = validar_cotacoes(
        tickers
    )


    segmentos, erros_segmentos = validar_segmentos(
        tickers
    )


    print()

    print(
        "========== RESUMO =========="
    )

    print(
        f"FIIs cadastrados: {len(tickers)}"
    )

    print(
        f"Cotações: {cotacoes}"
    )

    print(
        f"Classificados: {segmentos}"
    )


    print()


    if duplicados:

        logger.aviso(
            f"Tickers duplicados: {duplicados}"
        )

    else:

        logger.info(
            "Duplicados: OK"
        )



    if erros_cotacoes:

        logger.aviso(
            f"Cotações inválidas: {erros_cotacoes}"
        )

    else:

        logger.info(
            "Cotações: OK"
        )



    if erros_segmentos:

        logger.aviso(
            f"Segmentos inválidos: {erros_segmentos}"
        )

    else:

        logger.info(
            "Segmentos: OK"
        )


    print()

    logger.linha()



if __name__ == "__main__":

    executar()