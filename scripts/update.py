import requests

URL_B3 = "https://sistemaswebb3-listados.b3.com.br/fundsListedProxy/Search/GetDownload/eyJsYW5ndWFnZSI6InB0LWJyIiwidHlwZUZ1bmQiOiJGSUkifQ=="


r = requests.get(URL_B3)

print("Status:", r.status_code)
print("Content-Type:", r.headers.get("Content-Type"))
print("Content-Disposition:", r.headers.get("Content-Disposition"))
print("Tamanho:", len(r.content))

print("Primeiros bytes:")
print(r.content[:100])


with open("arquivo_b3", "wb") as f:
    f.write(r.content)
