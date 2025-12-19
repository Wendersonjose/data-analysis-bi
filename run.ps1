# Script PowerShell para executar a analise de extratos bancarios
# Uso: .\run.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Analise de Extratos Bancarios - Itau PJ" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se o Python esta instalado
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "OK Python encontrado: $pythonVersion" -ForegroundColor Green
}
else {
    Write-Host "ERRO Python nao encontrado. Instale o Python 3.11+ primeiro." -ForegroundColor Red
    exit 1
}

# Criar ambiente virtual se nao existir
if (!(Test-Path "venv")) {
    Write-Host ""
    Write-Host "Criando ambiente virtual..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "OK Ambiente virtual criado" -ForegroundColor Green
}

# Ativar ambiente virtual
Write-Host ""
Write-Host "Ativando ambiente virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Instalar/atualizar dependencias
Write-Host ""
Write-Host "Instalando dependencias..." -ForegroundColor Yellow
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt -q
Write-Host "OK Dependencias instaladas" -ForegroundColor Green

# Verificar se existem PDFs
$pdfCount = (Get-ChildItem -Path "pdfs" -Filter "*.pdf" -ErrorAction SilentlyContinue).Count
Write-Host ""
if ($pdfCount -eq 0) {
    Write-Host "PDFs encontrados na pasta 'pdfs': $pdfCount" -ForegroundColor Red
}
else {
    Write-Host "PDFs encontrados na pasta 'pdfs': $pdfCount" -ForegroundColor Green
}

if ($pdfCount -eq 0) {
    Write-Host ""
    Write-Host "ATENCAO: Nenhum PDF encontrado!" -ForegroundColor Yellow
    Write-Host "  Coloque os extratos bancarios em PDF na pasta 'pdfs' antes de executar." -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Deseja continuar mesmo assim? (s/n)"
    if ($response -ne "s" -and $response -ne "S") {
        Write-Host "Execucao cancelada." -ForegroundColor Yellow
        exit 0
    }
}

# Executar analise
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Iniciando analise..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

python -m src.main

# Verificar resultado
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  OK Analise concluida com sucesso!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Os resultados foram salvos em:" -ForegroundColor Cyan
    Write-Host "  - ./saida_analise/ (CSV e Excel)" -ForegroundColor White
    Write-Host "  - ./saida_analise/graficos/ (Graficos PNG)" -ForegroundColor White
    Write-Host ""
}
else {
    Write-Host ""
    Write-Host "ERRO durante a execucao. Verifique as mensagens acima." -ForegroundColor Red
    Write-Host ""
}
