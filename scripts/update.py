import json
from datetime import datetime
from pathlib import Path


# Pasta de saída do GitHub Pages
saida = Path("docs")

saida.mkdir(exist_ok=True)


# Lista inicial de teste
# Depois vamos substituir pela coleta da B3
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
    },
    {
        "codigo": "XPML11",
        "nome": "XP Malls",
        "segmento": "Shopping"
    }
]


arquivo = saida / "fiis.json"

with open(arquivo, "w", encoding="utf-8") as f:
    json.dump(
        {
            "atualizado": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "quantidade": len(fiis),
            "fiis": fiis
        },
        f,
        indent=4,
        ensure_ascii=False
    )


print(f"{arquivo} criado com {len(fiis)} FIIs")
