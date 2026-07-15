import requests
import pandas as pd
from pathlib import Path


URL_B3 = "https://sistemaswebb3-listados.b3.com.br/fundsListedProxy/Search/GetDownload/eyJsYW5ndWFnZSI6InB0LWJyIiwidHlwZUZ1bmQiOiJGSUkifQ=="


arquivo = Path("fundos_b3.csv")


# Baixa CSV da B3
r = requests.get(URL_B3)
r.raise_for_status()

with open(arquivo, "wb") as f:
    f.write(r.content)


print("Arquivo baixado:", arquivo)
print("Tamanho:", len(r.content), "bytes")


# Tenta ler CSV
df = pd.read_csv(
    arquivo,
    sep=";",
    encoding="utf-8"
)


print("\nCOLUNAS ENCONTRADAS:")
for coluna in df.columns:
    print("-", coluna)


print("\nPrimeiras linhas:")
print(df.head())
