#!/bin/bash
# Script de instalação do BackupMaster para Linux/Mac

echo "========================================"
echo " BackupMaster - Instalação"
echo "========================================"
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python não encontrado!"
    echo "Por favor, instale Python 3.8 ou superior"
    exit 1
fi

echo "[OK] Python encontrado"
echo ""

# Cria ambiente virtual
echo "Criando ambiente virtual..."
python3 -m venv venv

# Ativa ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Atualiza pip
echo "Atualizando pip..."
python -m pip install --upgrade pip

# Instala dependências
echo "Instalando dependências..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo " Instalação concluída com sucesso!"
echo "========================================"
echo ""
echo "Para usar o BackupMaster:"
echo ""
echo "1. Interface Gráfica (GUI):"
echo "   ./run_gui.sh"
echo ""
echo "2. Linha de Comando (CLI):"
echo "   ./run_cli.sh --help"
echo ""

# Cria atalhos
cat > run_gui.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python backupmaster_gui.py
EOF

cat > run_cli.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python backupmaster_cli.py "$@"
EOF

chmod +x run_gui.sh
chmod +x run_cli.sh

echo "Atalhos criados:"
echo "- run_gui.sh (Interface Gráfica)"
echo "- run_cli.sh (Linha de Comando)"
echo ""
