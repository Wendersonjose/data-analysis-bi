# 📊 Extrato Analytics - Análise de Extratos Bancários Itaú PJ

Sistema completo para análise automatizada de extratos bancários do Itaú Pessoa Jurídica em PDF. Extrai dados, categoriza transações, gera relatórios e visualizações.

## 🎯 Funcionalidades

- ✅ Leitura automática de PDFs (texto pesquisável)
- ✅ Extração de resumos mensais (entradas, saídas, saldos)
- ✅ Extração de transações individuais
- ✅ Categorização automática de transações
- ✅ Análises consolidadas (fluxo de caixa, rankings, Pareto)
- ✅ Exportação para CSV e Excel
- ✅ Geração de gráficos (PNG)
- ✅ Pronto para uso no Power BI

## 📁 Estrutura do Projeto

```
extrato-analytics/
├── README.md                 # Este arquivo
├── requirements.txt          # Dependências Python
├── .gitignore               # Arquivos ignorados pelo Git
├── run.ps1                  # Script de execução (PowerShell)
│
├── src/                     # Código fonte
│   ├── __init__.py
│   ├── config.py            # Configurações do projeto
│   ├── pdf_reader.py        # Leitor de PDFs
│   ├── parser_summary.py    # Parser de resumo mensal
│   ├── parser_transactions.py  # Parser de transações
│   ├── categorizer.py       # Categorizador automático
│   ├── analytics.py         # Análises e consolidações
│   ├── export.py            # Exportador CSV/Excel
│   ├── plots.py             # Gerador de gráficos
│   └── main.py              # Script principal
│
├── pdfs/                    # COLOQUE SEUS PDFs AQUI
│
├── saida_analise/           # Arquivos gerados (CSV/Excel)
│   └── graficos/            # Gráficos PNG
│
└── notebooks/               # Notebooks Jupyter (opcional)
    └── exploracao.ipynb
```

## 🚀 Como Usar (Windows)

### Passo 1: Preparar os PDFs

Coloque todos os extratos bancários em PDF na pasta `pdfs/`:

```
extrato-analytics/
└── pdfs/
    ├── extrato_jan_2025.pdf
    ├── extrato_fev_2025.pdf
    └── extrato_mar_2025.pdf
```

**Importante**: Os PDFs devem conter texto pesquisável (não apenas imagens escaneadas).

### Passo 2: Executar a Análise

Abra o PowerShell na pasta do projeto e execute:

```powershell
.\run.ps1
```

O script irá:
1. Criar ambiente virtual Python (se não existir)
2. Instalar dependências
3. Processar todos os PDFs
4. Gerar análises e relatórios
5. Criar gráficos

### Passo 3: Acessar os Resultados

Após a execução, os resultados estarão em:

```
saida_analise/
├── 01_resumo_mensal.csv
├── 02_movimentacoes.csv
├── 03_fluxo_caixa_mensal.csv
├── 04_saidas_por_categoria.csv
├── 05_entradas_por_categoria.csv
├── 06_top_saidas_descricao.csv
├── 07_top_entradas_descricao.csv
├── 08_indicadores.csv
├── analise_extratos.xlsx          # Todos os dados em uma planilha
│
└── graficos/
    ├── entradas_por_mes.png
    ├── saidas_por_mes.png
    ├── resultado_por_mes.png
    ├── top10_categorias_saida.png
    ├── top10_categorias_entrada.png
    └── pareto_saidas_categoria.png
```

## 📊 Análises Geradas

### 1. Resumo Mensal
- Depósitos e recebimentos
- Transferências (DOC/TED)
- Outras entradas
- Saques efetuados
- Débitos automáticos
- Outras saídas
- Totais de entradas e saídas
- Saldo inicial e final

### 2. Movimentações
Todas as transações extraídas com:
- Data
- Descrição
- Valor de entrada
- Valor de saída
- Saldo (quando disponível)
- Categoria automática

### 3. Fluxo de Caixa Mensal
- Entradas totais por mês
- Saídas totais por mês
- Resultado líquido
- Saldos inicial e final

### 4. Rankings por Categoria
- Saídas por categoria (total, quantidade, média)
- Entradas por categoria (total, quantidade, média)
- Análise de Pareto (80/20)

### 5. Top Descrições
- 50 principais descrições de saídas
- 50 principais descrições de entradas
- Útil para identificar padrões

### 6. Indicadores do Período
- Total de entradas
- Total de saídas
- Resultado líquido
- Médias mensais
- Número de meses analisados

## 🏷️ Categorias Automáticas

O sistema classifica automaticamente as transações nas seguintes categorias:

- **Fornecedores**: SISPAG FORNECEDORES, pagamentos a fornecedores
- **Tributos/Boletos**: Tributos municipais, DAS, DARF, boletos
- **PIX**: Transferências PIX, QR Code
- **Cartões**: Rede Visa, Mastercard, Elo, Amex
- **Tarifas Bancárias**: TAR PIX, tarifas, manutenção de conta
- **Débito Automático**: Pagamentos recorrentes
- **Saques**: Saque em caixa eletrônico, Banco24h
- **Depósitos**: Depósitos em dinheiro, cheque
- **Aplicações/Resgates**: Aplicações automáticas, resgates, rendimentos
- **Transferências**: DOC, TED
- **Recebimentos**: Créditos diversos
- **Outros**: Transações não classificadas

## 📈 Usando no Power BI

1. Abra o Power BI Desktop
2. Clique em "Obter Dados" → "Texto/CSV"
3. Selecione os arquivos CSV da pasta `saida_analise/`
4. Ou use o arquivo Excel consolidado `analise_extratos.xlsx`

**Dicas:**
- Use a coluna `mes_key` (YYYY-MM) para ordenação cronológica
- A coluna `categoria` permite filtros e segmentações
- Crie relacionamentos entre as tabelas usando `mes_key` e `arquivo`

## 🔧 Instalação Manual (Opcional)

Se preferir não usar o `run.ps1`:

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Executar análise
python -m src.main
```

## 📦 Dependências

- Python 3.11+
- pdfplumber >= 0.11.0 (leitura de PDFs)
- pandas >= 2.0.0 (análise de dados)
- openpyxl >= 3.1.0 (Excel)
- matplotlib >= 3.7.0 (gráficos)

## 🐛 Solução de Problemas

### PDFs não são processados
- Verifique se os PDFs contêm texto pesquisável (não são apenas imagens)
- Teste abrindo o PDF e tentando selecionar/copiar texto
- Se necessário, use OCR para converter PDFs escaneados

### Valores não são extraídos corretamente
- O parser foi otimizado para extratos Itaú PJ
- Layouts muito diferentes podem requerer ajustes no código
- Verifique os logs para identificar problemas específicos

### Erros de instalação
- Certifique-se de ter Python 3.11+ instalado
- Use `python --version` para verificar
- No Windows, pode ser necessário executar: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

### Ambiente virtual não ativa
```powershell
# Permitir execução de scripts
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Ativar manualmente
.\venv\Scripts\Activate.ps1
```

## 🎓 Exploração Adicional

Use o notebook Jupyter para análises exploratórias:

```powershell
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Instalar Jupyter (se necessário)
pip install jupyter

# Abrir notebook
jupyter notebook notebooks/exploracao.ipynb
```

## 📝 Notas Importantes

1. **Privacidade**: Este projeto processa dados localmente. Nenhum dado é enviado para servidores externos.

2. **Git**: Os PDFs e arquivos de saída estão no `.gitignore` por padrão. Remova essas entradas se desejar versioná-los.

3. **Personalização**: As regras de categorização estão em `src/categorizer.py` e podem ser ajustadas conforme necessário.

4. **Performance**: O processamento é rápido para volumes moderados (< 100 PDFs). Para volumes maiores, considere processamento paralelo.

## 🤝 Contribuições

Este é um projeto interno/educacional. Sugestões e melhorias são bem-vindas!

## 📄 Licença

Uso interno. Dados bancários são confidenciais.

---

**Desenvolvido para análise de extratos bancários Itaú PJ**

*Versão 1.0.0*
