from pathlib import Path

# ===========================
# Pastas
# ===========================

ROOT = Path(__file__).resolve().parent.parent

DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

LOGS = ROOT / "logs"
LOGS.mkdir(exist_ok=True)

# ===========================
# Arquivos
# ===========================

FIIS_JSON = DOCS / "fiis.json"
COTACOES_JSON = DOCS / "cotacoes.json"
VERSION_JSON = DOCS / "version.json"

FALHAS_TXT = LOGS / "falhas.txt"

# ===========================
# B3
# ===========================

URL_B3 = (
    "https://sistemaswebb3-listados.b3.com.br/"
    "fundsListedProxy/Search/GetDownload/"
    "eyJsYW5ndWFnZSI6InB0LWJyIiwidHlwZUZ1bmQiOiJGSUkifQ=="
)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
    "Referer": "https://www.b3.com.br/"
}

# ===========================
# Yahoo
# ===========================

LOTE = 100
PERIODO = "7d"

# ===========================
# Projeto
# ===========================

VERSAO = 1
ORIGEM = "B3"