import json


with open(
    "docs/indicadores.json",
    encoding="utf-8"
) as f:

    dados = json.load(f)


for ticker in [
    "MXRF11",
    "HGLG11",
    "XPML11",
    "KNCR11"
]:

    print()
    print("=" * 40)
    print(ticker)

    print(
        dados["dados"].get(ticker)
    )