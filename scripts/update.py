import requests
import base64
import pandas as pd
from io import StringIO


URL_B3 = "https://sistemaswebb3-listados.b3.com.br/fundsListedProxy/Search/GetDownload/eyJsYW5ndWFnZSI6InB0LWJyIiwidHlwZUZ1bmQiOiJGSUkifQ=="


headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
    "Referer": "https://www.b3.com.br/"
}


r = requests.get(URL_B3, headers=headers)

r.raise_for_status()


# resposta da B3 em Base64
texto_base64 = r.text


# decodifica
csv_bytes = base64.b64decode(texto_base64)


# transforma em texto
csv_texto = csv_bytes.decode(
    "utf-8",
    errors="ignore"
)


print(csv_texto[:500])


# lê CSV
df = pd.read_csv(
    StringIO(csv_texto),
    sep=";"
)


print("\nCOLUNAS:")
print(df.columns.tolist())


print("\nPRIMEIROS REGISTROS:")
print(df.head())
