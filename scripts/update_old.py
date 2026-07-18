import requests
import base64
from io import StringIO

import pandas as pd

from config import URL_B3, FIIS_JSON
from utils import salvar_json, agora_iso
from logger import info, aviso, separador, finalizar


def baixar_b3():

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Referer": "https://www.b3.com.br"
    }

    resposta = requests.get(
        URL_B3,
        headers=headers,
        timeout=30
    )

    resposta.raise_for_status()

    return resposta.text



def ler_csv(texto_base64):

    dados = base64.b64decode(texto_base64)

    texto = dados.decode("latin1")

    linhas = [
        linha
        for linha in texto.splitlines()
        if linha.strip()
    ]

    texto = "\n".join(linhas)


    df = pd.read_csv(
    StringIO(texto),
    sep=";",
    header=0,
    index_col=False,
    engine="python"
)

    # garante que não use coluna como índice
    df.reset_index(drop=True, inplace=True)


    # somente as três colunas necessárias

    df = df.iloc[:, :3]


    return df



def gerar_fiis(df):

    df.columns = [
        coluna.strip()
        for coluna in df.columns
    ]


    df.rename(
        columns={
            "Razão Social": "razao_social",
            "Fundo": "nome",
            "Código": "codigo"
        },
        inplace=True
    )

    print(df.head())
    print(df.columns.tolist())
    print(df["codigo"].head())


    df = df.dropna(
        subset=["codigo"]
    )


    lista = []


    for _, linha in df.iterrows():

        lista.append(
            {
                "codigo":
                    str(linha["codigo"]).strip(),

                "nome":
                    str(linha["nome"]).strip(),

                "razao_social":
                    str(linha["razao_social"]).strip()
            }
        )


    return lista



def atualizar():

    info("Baixando lista de FIIs da B3...")


    dados = baixar_b3()


    info("Lendo CSV...")


    df = ler_csv(dados)


    info(
        f"Registros encontrados: {len(df)}"
    )


    fiis = gerar_fiis(df)


    resultado = {

        "versao": 1,

        "gerado_em":
            agora_iso(),

        "origem":
            "B3",

        "quantidade":
            len(fiis),

        "dados":
            fiis
    }


    salvar_json(
        FIIS_JSON,
        resultado
    )


    separador()

    info(
        f"FIIs salvos: {len(fiis)}"
    )

    info(
        f"Arquivo: {FIIS_JSON}"
    )



if __name__ == "__main__":

    try:

        atualizar()

        finalizar()


    except Exception as e:

        aviso(
            f"Falha: {e}"
        )

        raise