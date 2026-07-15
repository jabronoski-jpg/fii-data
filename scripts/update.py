import requests
import json
from datetime import datetime
from pathlib import Path


saida = Path("docs")
saida.mkdir(exist_ok=True)


def salvar_json(nome, dados):
    arquivo = saida / nome

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(
            dados,
            f,
            indent=4,
            ensure_ascii=False
        )


# teste inicial
# depois substituímos pela fonte B3

fiis = [
    {
        "codigo": "MXRF11",
        "nome": "Maxi Renda",
        "segmento": "Papel"
    },
    {
        "codigo": "HGLG11",
        "nome": "CSHG Logística",
        "segmento": "Logística"
    }
]


resultado = {
    "atualizado": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "quantidade": len(fiis),
    "fiis": fiis
}


salvar_json("fiis.json", resultado)

print("FIIs atualizados:", len(fiis))
