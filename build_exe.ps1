# ==============================
# build_exe.ps1
# Script para gerar EXE no Windows
# ==============================

$ErrorActionPreference = "Stop"

Write-Host "======================================="
Write-Host " Criando executavel do projeto"
Write-Host "======================================="

# 1. Verificar Python
Write-Host "Verificando Python..."
$python = Get-Command python -ErrorAction SilentlyContinue

if (-not $python) {
    Write-Host "ERRO: Python nao encontrado."
    Write-Host "Instale em: https://www.python.org/downloads/windows/"
    Write-Host "Marque a opcao 'Add Python to PATH'"
    exit 1
}

Write-Host "Python encontrado."

# 2. Criar ambiente virtual
if (-not (Test-Path ".venv")) {
    Write-Host "Criando ambiente virtual..."
    python -m venv .venv
}

# 3. Ativar ambiente virtual
Write-Host "Ativando ambiente virtual..."
& .\.venv\Scripts\Activate.ps1

# 4. Atualizar pip
Write-Host "Atualizando pip..."
python -m pip install --upgrade pip

# 5. Instalar dependencias
Write-Host "Instalando dependencias..."
pip install -r requirements.txt
pip install pyinstaller

# 6. Limpar builds antigos
if (Test-Path "build") { Remove-Item build -Recurse -Force }
if (Test-Path "dist")  { Remove-Item dist -Recurse -Force }

# 7. Gerar executavel
Write-Host "Gerando executavel..."
pyinstaller `
    --onefile `
    --name lactanet_extraction `
    main.py

Write-Host ""
Write-Host "======================================="
Write-Host " Executavel criado com sucesso!"
Write-Host " Caminho:"
Write-Host " dist\lactanet_extraction.exe"
Write-Host "======================================="
