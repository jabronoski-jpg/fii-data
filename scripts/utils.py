import json
from datetime import datetime, timezone


def carregar_json(caminho):
    """Carrega um arquivo JSON."""

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_json(caminho, objeto):
    """Salva um objeto em formato JSON."""

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(
            objeto,
            f,
            indent=4,
            ensure_ascii=False
        )


def dividir_em_lotes(lista, tamanho):
    """Divide uma lista em blocos."""

    for i in range(0, len(lista), tamanho):
        yield lista[i:i+tamanho]


def agora_iso():
    """Data e hora UTC no formato ISO."""

    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )