import json

with open(
    "docs/fiis.json",
    encoding="utf-8"
) as f:

    dados = json.load(f)


for fii in dados["dados"]:

    if fii["ticker"] == "MAGM11":

        print(fii)