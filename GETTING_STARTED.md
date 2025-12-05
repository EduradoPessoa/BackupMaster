# 🔄 BackupMaster - Instalação e Primeiros Passos

## 📦 O que foi criado?

O **BackupMaster** é um sistema profissional de backup com as seguintes características:

### ✨ Recursos Principais

1. **🧠 Backup Inteligente**
   - Sistema incremental que copia apenas arquivos modificados
   - Economiza tempo e espaço em disco
   - Usa hash MD5 para detectar mudanças

2. **🖥️ Multi-Plataforma**
   - Windows, Linux e Mac
   - Interface gráfica (GUI) moderna e intuitiva
   - Interface de linha de comando (CLI) completa

3. **🆓 100% Gratuito**
   - Software livre e open source
   - Licença MIT - use sem limitações
   - Sem restrições em empresas ou projetos pessoais

4. **🗜️ Múltiplos Compactadores**
   - **ZIP** - Compatibilidade universal
   - **7z** - Máxima compressão (até 45% de economia)
   - **TAR.GZ** - Padrão Linux/Unix
   - **TAR.BZ2** - Alta compressão

5. **🎯 System Tray**
   - Ícone na bandeja do sistema Windows
   - Notificações de progresso
   - Minimiza para tray ao invés de fechar

## 📁 Estrutura do Projeto

```
wsp2/
├── backupmaster/           # Pacote principal
│   ├── __init__.py        # Inicialização do pacote
│   └── core.py            # Motor de backup
├── backupmaster_gui.py    # Interface gráfica (PyQt6)
├── backupmaster_cli.py    # Interface de linha de comando
├── test_backupmaster.py   # Suite de testes
├── requirements.txt       # Dependências Python
├── install.bat           # Instalador Windows
├── install.sh            # Instalador Linux/Mac
├── README.md             # Documentação principal
├── USAGE.md              # Guia de uso completo
├── EXAMPLES.md           # Exemplos práticos
├── LICENSE               # Licença MIT
└── .gitignore           # Arquivos ignorados pelo Git
```

## 🚀 Instalação Rápida

### Windows

1. **Execute o instalador:**
   ```cmd
   install.bat
   ```

2. **O instalador irá:**
   - Verificar se Python está instalado
   - Criar ambiente virtual
   - Instalar todas as dependências
   - Criar atalhos para GUI e CLI

### Linux/Mac

1. **Dê permissão de execução:**
   ```bash
   chmod +x install.sh
   ```

2. **Execute o instalador:**
   ```bash
   ./install.sh
   ```

## 💻 Como Usar

### Interface Gráfica (Recomendado para iniciantes)

#### Windows
```cmd
run_gui.bat
```

#### Linux/Mac
```bash
./run_gui.sh
```

**Ou manualmente:**
```bash
# Ative o ambiente virtual
# Windows:
venv\Scripts\activate.bat

# Linux/Mac:
source venv/bin/activate

# Execute a GUI
python backupmaster_gui.py
```

### Interface de Linha de Comando (CLI)

#### Criar Backup
```bash
python backupmaster_cli.py backup \
  --source "C:/Documentos" \
  --dest "D:/Backups" \
  --format 7z \
  --incremental
```

#### Listar Backups
```bash
python backupmaster_cli.py list --dest "D:/Backups"
```

#### Restaurar Backup
```bash
python backupmaster_cli.py restore \
  --backup "D:/Backups/backup.7z" \
  --dest "C:/Restaurar"
```

#### Ver Ajuda
```bash
python backupmaster_cli.py --help
python backupmaster_cli.py backup --help
```

## 🧪 Testar o Sistema

Execute a suite de testes para verificar se tudo está funcionando:

```bash
# Ative o ambiente virtual primeiro
python test_backupmaster.py
```

Os testes irão verificar:
- ✅ Criação de backup
- ✅ Backup incremental
- ✅ Múltiplos formatos de compressão
- ✅ Restauração de backup
- ✅ Listagem de backups

## 📊 Exemplo Prático

### Cenário: Backup Diário de Documentos

1. **Primeiro Backup (Completo)**
   ```bash
   python backupmaster_cli.py backup \
     -s "C:/Users/Usuario/Documentos" \
     -d "D:/Backups" \
     -f 7z \
     -i
   ```
   - Copia todos os arquivos
   - Cria arquivo: `Documentos_incremental_20251205_140000.7z`
   - Economia de espaço: ~45%

2. **Backups Seguintes (Incrementais)**
   ```bash
   python backupmaster_cli.py backup \
     -s "C:/Users/Usuario/Documentos" \
     -d "D:/Backups" \
     -f 7z \
     -i
   ```
   - Copia apenas arquivos modificados
   - Muito mais rápido
   - Economiza espaço

3. **Restaurar Backup**
   ```bash
   # Listar backups disponíveis
   python backupmaster_cli.py list -d "D:/Backups"
   
   # Restaurar backup específico
   python backupmaster_cli.py restore \
     -b "D:/Backups/Documentos_incremental_20251205_140000.7z" \
     -d "C:/Restaurar"
   ```

## 🎨 Interface Gráfica

A interface gráfica oferece:

- **Design Moderno**: Tema escuro com gradientes e cores vibrantes
- **Fácil de Usar**: Interface intuitiva e simples
- **Progresso em Tempo Real**: Barra de progresso e status
- **Histórico Visual**: Tabela com todos os backups
- **System Tray**: Minimiza para bandeja do sistema
- **Notificações**: Alertas quando backup é concluído

### Recursos da GUI:

1. **Configuração de Backup**
   - Selecionar pasta de origem
   - Selecionar pasta de destino
   - Escolher formato de compressão
   - Ativar backup incremental

2. **Monitoramento**
   - Barra de progresso visual
   - Status em tempo real
   - Estatísticas de economia de espaço

3. **Histórico**
   - Tabela com todos os backups
   - Informações detalhadas
   - Restauração com um clique

4. **System Tray**
   - Ícone na bandeja
   - Menu de contexto
   - Notificações do sistema

## 🔧 Automação

### Agendar Backups Automáticos

#### Windows (Task Scheduler)

1. Abra o Agendador de Tarefas
2. Crie nova tarefa
3. Configure:
   - **Gatilho**: Diariamente às 02:00
   - **Ação**: Iniciar programa
   - **Programa**: `C:\caminho\para\venv\Scripts\python.exe`
   - **Argumentos**: `backupmaster_cli.py backup -s "C:/Documentos" -d "D:/Backups" -f 7z -i`
   - **Iniciar em**: `C:\caminho\para\wsp2`

#### Linux/Mac (Cron)

```bash
# Editar crontab
crontab -e

# Adicionar linha para backup diário às 2h
0 2 * * * cd /caminho/para/wsp2 && ./venv/bin/python backupmaster_cli.py backup -s "/home/usuario/documentos" -d "/backup" -f 7z -i
```

## 📚 Documentação Adicional

- **README.md** - Visão geral do projeto
- **USAGE.md** - Guia completo de uso
- **EXAMPLES.md** - Exemplos práticos
- **LICENSE** - Licença MIT

## 🆘 Solução de Problemas

### Erro: "Python não encontrado"
- Instale Python 3.8+ de https://www.python.org/
- Certifique-se de marcar "Add to PATH" durante instalação

### Erro: "Módulo não encontrado"
```bash
# Ative o ambiente virtual
venv\Scripts\activate.bat  # Windows
source venv/bin/activate   # Linux/Mac

# Reinstale dependências
pip install -r requirements.txt
```

### Backup muito lento
- Use backup incremental (`-i`)
- Escolha formato ZIP para velocidade
- Evite pastas com muitos arquivos pequenos

### Interface gráfica não abre
```bash
# Verifique se PyQt6 está instalado
pip install PyQt6

# Execute com mensagens de erro
python backupmaster_gui.py
```

## 🎯 Próximos Passos

1. **Teste o sistema** com a suite de testes
2. **Crie seu primeiro backup** usando a GUI
3. **Configure backups automáticos** para suas pastas importantes
4. **Explore a CLI** para automação avançada
5. **Leia a documentação** completa em USAGE.md

## 💡 Dicas

- ✅ Use backup incremental para backups diários
- ✅ Formato 7z oferece melhor compressão
- ✅ Mantenha backups em múltiplos locais
- ✅ Teste restaurações periodicamente
- ✅ Monitore o espaço em disco

## 📞 Suporte

- **Documentação**: Consulte README.md, USAGE.md e EXAMPLES.md
- **Testes**: Execute test_backupmaster.py
- **Código**: Todo código está comentado e documentado

---

**BackupMaster v1.0.0** - Sistema Profissional de Backup
Desenvolvido com ❤️ em Python
