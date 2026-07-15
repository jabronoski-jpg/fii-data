import requests
import pandas as pd
import json
from datetime import datetime
from pathlib import Path


PASTA_SAIDA = Path("docs")
PASTA_SAIDA.mkdir(exist_ok=True)


def salvar_json(nome, dados):
    arquivo = PASTA_SAIDA / nome

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(
            dados,
            f,
            indent=4,
            ensure_ascii=False
        )


def baixar_arquivo(url):
    resposta = requests.get(url)
    resposta.raise_for_status()

    nome = "fundos_b3.xlsx"

    with open(nome, "wb") as f:
        f.write(resposta.content)

    return nome


def gerar_lista_fiis(arquivo):

    df = pd.read_excel(arquivo)

    print("Colunas encontradas:")
    print(df.columns)


    # Ajustar conforme os nomes reais da B3

    df = df[
        df["Tipo de Fundo"].str.contains(
            "FII",
            na=False
        )
    ]


    # remover cancelados
    if "Situação" in df.columns:
        df = df[
            df["Situação"] == "ATIVO"
        ]


    lista = []

    for _, linha in df.iterrows():

        lista.append(
            {
                "codigo": linha["Código"],
                "nome": linha["Nome"],
                "segmento": linha.get(
                    "Segmento",
                    ""
                )
            }
        )


    return lista



# endereço do arquivo B3
URL_B3 = "COLOCAR_URL_DA_B3_AQUI"


try:

    arquivo = baixar_arquivo(URL_B3)

    fiis = gerar_lista_fiis(arquivo)


    resultado = {

        "atualizado":
            datetime.now()
            .strftime("%Y-%m-%d %H:%M:%S"),

        "quantidade":
            len(fiis),

        "fiis":
            fiis
    }


    salvar_json(
        "fiis.json",
        resultado
    )


    print(
        "FIIs gerados:",
        len(fiis)
    )


except Exception as erro:

    print(
        "Erro:",
        erro
    )

    raise
