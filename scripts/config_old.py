from pathlib import Path

# ==========================
# Diretórios
# ==========================

ROOT = Path(__file__).resolve().parent.parent

SCRIPTS = ROOT / "scripts"
DOCS = ROOT / "docs"

# ==========================
# Arquivos JSON
# ==========================

FIIS_JSON = DOCS / "fiis.json"
COTACOES_JSON = DOCS / "cotacoes.json"
DIVIDENDOS_JSON = DOCS / "dividendos.json"
VERSION_JSON = DOCS / "version.json"

# Arquivos auxiliares
FALHAS_TXT = DOCS / "falhas.txt"

# ==========================
# Configurações
# ==========================

LOTE = 100
TIMEOUT = 30

# ==========================
# URLs
# ==========================

URL_B3 = (
    "https://sistemaswebb3-listados.b3.com.br/"
    "fundsListedProxy/Search/GetDownload/"
    "eyJsYW5ndWFnZSI6InB0LWJyIiwidHlwZUZ1bmQiOiJGSUkifQ=="
)