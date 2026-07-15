from datetime import datetime
import json

dados = {
    "ultima_atualizacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "status": "OK"
}

with open("public/version.json", "w", encoding="utf-8") as arquivo:
    json.dump(dados, arquivo, indent=4, ensure_ascii=False)

print("Arquivo version.json atualizado!")
