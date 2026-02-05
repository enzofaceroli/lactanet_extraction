Write-Host "=============================================="
Write-Host " Gerador de Executável (Windows)"
Write-Host "=============================================="
Write-Host ""

# ------------------------------------------------
# 1. Verificar Python
# ------------------------------------------------
$python = Get-Command python -ErrorAction SilentlyContinue

if (-not $python) {
    Write-Host "❌ Python não encontrado."
    Write-Host ""
    Write-Host "➡️  Instale o Python 3 em:"
    Write-Host "   https://www.python.org/downloads/windows/"
    Write-Host ""
    Write-Host "⚠️  IMPORTANTE:"
    Write-Host "   Marque a opção 'Add Python to PATH'"
    Write-Host ""
    Pause
    exit 1
}

Write-Host "✔ Python encontrado: $(python --version)"
Write-Host ""

# ------------------------------------------------
# 2. Garantir pip atualizado
# ------------------------------------------------
Write-Host "🔄 Atualizando pip..."
python -m pip install --upgrade pip

# ------------------------------------------------
# 3. Verificar / instalar uv
# ------------------------------------------------
$uv = Get-Command uv -ErrorAction SilentlyContinue

if (-not $uv) {
    Write-Host "⚠️  uv não encontrado. Instalando..."
    python -m pip install uv
} else {
    Write-Host "✔ uv encontrado: $(uv --version)"
}

Write-Host ""

# ------------------------------------------------
# 4. Criar ambiente virtual
# ------------------------------------------------
if (-not (Test-Path ".venv")) {
    Write-Host "🔧 Criando ambiente virtual..."
    uv venv
} else {
    Write-Host "✔ Ambiente virtual já existe"
}

Write-Host ""

# ------------------------------------------------
# 5. Instalar dependências
# ------------------------------------------------
Write-Host "📦 Instalando dependências..."
uv sync

Write-Host ""

# ------------------------------------------------
# 6. Garantir PyInstaller
# ------------------------------------------------
Write-Host "📦 Instalando PyInstaller..."
uv pip install pyinstaller

Write-Host ""

# ------------------------------------------------
# 7. Gerar executável
# ------------------------------------------------
Write-Host "⚙️  Gerando executável..."

uv run pyinstaller `
    --onefile `
    --name MeuPrograma `
    main.py

Write-Host ""

# ------------------------------------------------
# 8. Resultado final
# ------------------------------------------------
Write-Host "=============================================="
Write-Host " ✅ EXECUTÁVEL GERADO COM SUCESSO"
Write-Host "=============================================="
Write-Host ""
Write-Host "📁 Arquivo gerado:"
Write-Host "   dist\MeuPrograma.exe"
Write-Host ""
Write-Host "👉 Você pode enviar esse arquivo para qualquer pessoa."
Write-Host "   Não é necessário Python no computador de destino."
Write-Host ""

Pause
