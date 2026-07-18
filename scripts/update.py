import base64
import json
from datetime import datetime
from io import StringIO

from numpy import rint
import pandas as pd
import requests

import config
import logger


def baixar_b3():

    resposta = requests.get(
        config.URL_B3,
        headers=config.HEADERS,
        timeout=30
    )

    resposta.raise_for_status()

    return resposta.text


def ler_csv(texto_base64):

    dados = base64.b64decode(texto_base64)

    texto = dados.decode("latin1").lstrip()

    linhas = [
        linha
        for linha in texto.splitlines()
        if linha.strip()
    ]

    texto = "\n".join(linhas)

# A B3 gera um ';' extra ao final de cada linha do CSV.
# Removemos esse caractere para evitar que versões mais novas
# do pandas interpretem a primeira coluna como índice.
    texto = "\n".join(
    linha.rstrip(";")
    for linha in linhas
    )
    

    df = pd.read_csv(
    StringIO(texto),
    sep=";",
    engine="python"
)

    print(df.head())

    print(df.columns.tolist())

    print(df.iloc[0].tolist())

    df = df.iloc[:, :3]

    df.columns = [c.strip() for c in df.columns]

    return df


def preparar(df):

    df = df.rename(
        columns={
            "Razão Social": "razao_social",
            "Fundo": "nome",
            "Código": "codigo"
        }
    )

    df = df.reset_index(drop=True)

    df["codigo"] = df["codigo"].astype(str).str.strip()

    df["ticker"] = df["codigo"] + "11"

    return df


def gerar(df):

    lista = []

    for _, linha in df.iterrows():

        lista.append(
            {
                "codigo": linha["codigo"],
                "ticker": linha["ticker"],
                "nome": linha["nome"].strip(),
                "razao_social": linha["razao_social"].strip()
            }
        )

    return lista


def salvar(lista):

    resultado = {

        "versao": config.VERSAO,

        "gerado_em": datetime.utcnow().strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),

        "origem": config.ORIGEM,

        "quantidade": len(lista),

        "dados": lista
    }

    with open(
        config.FIIS_JSON,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            resultado,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


def atualizar():

    logger.linha()

    logger.info("Baixando lista de FIIs da B3...")

    texto = baixar_b3()

    logger.info("Lendo CSV...")

    df = ler_csv(texto)

    logger.info(f"Registros encontrados: {len(df)}")

    df = preparar(df)

    lista = gerar(df)

    salvar(lista)

    logger.linha()

    logger.info(f"FIIs salvos: {len(lista)}")

    logger.info(f"Arquivo: {config.FIIS_JSON}")

    logger.linha()


if __name__ == "__main__":

    atualizar()