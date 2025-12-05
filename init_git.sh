#!/bin/bash
# Script para inicializar repositório Git e preparar para GitHub

echo "========================================"
echo " BackupMaster - Inicializar Git"
echo "========================================"
echo ""

# Verifica se Git está instalado
if ! command -v git &> /dev/null; then
    echo "[ERRO] Git não encontrado!"
    echo "Por favor, instale Git de https://git-scm.com/"
    exit 1
fi

echo "[OK] Git encontrado"
echo ""

# Inicializa repositório
echo "Inicializando repositório Git..."
git init

# Adiciona todos os arquivos
echo "Adicionando arquivos..."
git add .

# Primeiro commit
echo "Criando primeiro commit..."
git commit -m "Initial commit: BackupMaster v1.0.0 - Sistema Profissional de Backup"

echo ""
echo "========================================"
echo " Repositório Git inicializado!"
echo "========================================"
echo ""
echo "Próximos passos:"
echo ""
echo "1. Crie um repositório no GitHub:"
echo "   https://github.com/new"
echo ""
echo "2. Configure o remote:"
echo "   git remote add origin https://github.com/SEU-USUARIO/backupmaster.git"
echo ""
echo "3. Envie para o GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "Ou execute:"
echo "   ./setup_github.sh"
echo ""
