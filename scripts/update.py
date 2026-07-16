import requests
import base64
import json
from datetime import datetime
from io import StringIO
from pathlib import Path

import pandas as pd


# Endpoint B3 - Fundos Imobiliários
URL_B3 = (
    "https://sistemaswebb3-listados.b3.com.br/"
    "fundsListedProxy/Search/GetDownload/"
    "eyJsYW5ndWFnZSI6InB0LWJyIiwidHlwZUZ1bmQiOiJGSUkifQ=="
)


PASTA_SAIDA = Path("docs")
PASTA_SAIDA.mkdir(exist_ok=True)


def baixar_b3():

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Referer": "https://www.b3.com.br/"
    }

    resposta = requests.get(
        URL_B3,
        headers=headers
    )

    resposta.raise_for_status()

    return resposta.text



def ler_csv_b3(texto_base64):

    # Decodifica Base64
    dados = base64.b64decode(
        texto_base64
    )


    # Converte para texto
    texto_csv = dados.decode(
        "latin1"
    )


    df = pd.read_csv(
        StringIO(texto_csv),
        sep=";",
        engine="python"
    )


    return df



def gerar_json(df):

    # Remove espaços dos nomes das colunas
    df.columns = [
        c.strip()
        for c in df.columns
    ]


    # Corrige nomes vindos da B3
    df.rename(
        columns={
            "Razão Social": "razao_social",
            "Fundo": "nome",
            "Código": "codigo"
        },
        inplace=True
    )

    print("\nANTES DO FILTRO:")
    print(df.head(10))

    print("\nVALORES CODIGO:")
    print(df["codigo"].head(10))


    # Remove linhas sem código
    df = df.dropna(
        subset=["codigo"]
    )


    lista = []


    for _, linha in df.iterrows():

        lista.append(
            {
                "codigo": str(
                    linha["codigo"]
                ).strip(),

                "nome": str(
                    linha["nome"]
                ).strip(),

                "razao_social": str(
                    linha["razao_social"]
                ).strip()
            }
        )


    return lista



def salvar_json(lista):

    resultado = {

        "atualizado":
            datetime.now()
            .strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "quantidade":
            len(lista),

        "fiis":
            lista
    }


    arquivo = (
        PASTA_SAIDA /
        "fiis.json"
    )


    with open(
        arquivo,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            resultado,
            f,
            indent=4,
            ensure_ascii=False
        )


    print(
        "Arquivo criado:",
        arquivo
    )

    print(
        "Quantidade de FIIs:",
        len(lista)
    )



# ==========================
# EXECUÇÃO
# ==========================

try:

    print("Baixando dados da B3...")

    dados = baixar_b3()


    print("Lendo CSV...")

    df = ler_csv_b3(
        dados
    )


    print("Colunas:")
    print(
        df.columns.tolist()
    )


    fiis = gerar_json(
        df
    )


    salvar_json(
        fiis
    )


except Exception as erro:

    print(
        "ERRO:",
        erro
    )

    raise
