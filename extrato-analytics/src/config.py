"""
Configurações do projeto de análise de extratos bancários.
"""

from pathlib import Path

# Caminhos do projeto
PROJECT_ROOT = Path(__file__).parent.parent
PDFS_DIR = PROJECT_ROOT / "pdfs"
OUTPUT_DIR = PROJECT_ROOT / "saida_analise"
GRAFICOS_DIR = OUTPUT_DIR / "graficos"

# Criar diretórios de saída se não existirem
OUTPUT_DIR.mkdir(exist_ok=True)
GRAFICOS_DIR.mkdir(exist_ok=True)

# Configurações de análise
MESES_PT = {
    "jan": "01", "fev": "02", "mar": "03", "abr": "04",
    "mai": "05", "jun": "06", "jul": "07", "ago": "08",
    "set": "09", "out": "10", "nov": "11", "dez": "12"
}

# Palavras-chave para identificar resumo mensal
RESUMO_KEYWORDS = [
    "depositos", "recebimentos", "transferencias", "doc", "ted",
    "outras entradas", "saques efetuados", "debitos automaticos",
    "outras saidas", "total de entradas", "total de saidas"
]

# Configuração de logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"
