# 🚀 BackupMaster - Guia Rápido

## ⚡ Início em 3 Passos

### 1️⃣ Instalar (1 minuto)
```bash
# Windows
install.bat

# Linux/Mac
chmod +x install.sh && ./install.sh
```

### 2️⃣ Executar Interface Gráfica
```bash
# Windows
run_gui.bat

# Linux/Mac  
./run_gui.sh
```

### 3️⃣ Criar Backup
1. Clique em "Procurar" ao lado de **Origem**
2. Selecione a pasta que deseja fazer backup
3. Clique em "Procurar" ao lado de **Destino**
4. Selecione onde salvar o backup
5. Escolha o formato (recomendado: **7z**)
6. Marque **Backup Incremental** para backups mais rápidos
7. Clique em **🚀 Iniciar Backup**

## 📋 Comandos CLI Essenciais

### Criar Backup
```bash
# Backup completo
python backupmaster_cli.py backup -s "C:/Documentos" -d "D:/Backups" -f 7z

# Backup incremental (mais rápido)
python backupmaster_cli.py backup -s "C:/Documentos" -d "D:/Backups" -f 7z -i
```

### Listar Backups
```bash
python backupmaster_cli.py list -d "D:/Backups"
```

### Restaurar Backup
```bash
python backupmaster_cli.py restore -b "D:/Backups/backup.7z" -d "C:/Restaurar"
```

### Ver Ajuda
```bash
python backupmaster_cli.py --help
python backupmaster_cli.py info
```

## 🎯 Casos de Uso Comuns

### 📁 Backup Diário de Documentos
```bash
# Primeiro backup (completo)
python backupmaster_cli.py backup -s "C:/Users/Usuario/Documentos" -d "D:/Backups" -f 7z -i

# Backups seguintes (apenas arquivos modificados)
# Use o mesmo comando - o sistema detecta automaticamente!
python backupmaster_cli.py backup -s "C:/Users/Usuario/Documentos" -d "D:/Backups" -f 7z -i
```

### 📸 Backup de Fotos
```bash
# Use 7z para máxima compressão
python backupmaster_cli.py backup -s "C:/Fotos" -d "E:/Backups/Fotos" -f 7z
```

### 💻 Backup de Projeto
```bash
# ZIP para acesso rápido
python backupmaster_cli.py backup -s "C:/Projetos/MeuApp" -d "D:/Backups" -f zip -i
```

## 🗜️ Qual Formato Usar?

| Situação | Formato Recomendado | Por quê? |
|----------|-------------------|----------|
| Backup diário | **7z** + incremental | Máxima economia de espaço |
| Acesso frequente | **ZIP** | Compatibilidade universal |
| Servidor Linux | **TAR.GZ** | Padrão Unix |
| Arquivos grandes | **7z** | Melhor compressão |
| Velocidade | **ZIP** | Mais rápido |

## ⏰ Automatizar Backups

### Windows - Criar Tarefa Agendada

1. **Abrir Agendador de Tarefas**
   - Pressione `Win + R`
   - Digite `taskschd.msc`
   - Enter

2. **Criar Nova Tarefa**
   - Clique em "Criar Tarefa Básica"
   - Nome: "Backup Diário"
   - Gatilho: "Diariamente" às 02:00

3. **Configurar Ação**
   - Ação: "Iniciar um programa"
   - Programa: `C:\caminho\para\wsp2\venv\Scripts\python.exe`
   - Argumentos: `backupmaster_cli.py backup -s "C:/Documentos" -d "D:/Backups" -f 7z -i`
   - Iniciar em: `C:\caminho\para\wsp2`

### Linux/Mac - Usar Cron

```bash
# Editar crontab
crontab -e

# Adicionar linha (backup diário às 2h)
0 2 * * * cd /caminho/para/wsp2 && ./venv/bin/python backupmaster_cli.py backup -s "/home/usuario/documentos" -d "/backup" -f 7z -i
```

## 🎨 Recursos da Interface Gráfica

### Janela Principal
- ✅ Seleção visual de pastas
- ✅ Escolha de formato com dropdown
- ✅ Checkbox para backup incremental
- ✅ Barra de progresso em tempo real
- ✅ Tabela de histórico de backups

### System Tray (Bandeja do Sistema)
- ✅ Ícone laranja na bandeja
- ✅ Clique direito para menu
- ✅ Duplo clique para mostrar/ocultar
- ✅ Notificações quando backup completa
- ✅ Não fecha ao clicar X (minimiza)

### Histórico de Backups
- ✅ Ver todos os backups criados
- ✅ Informações detalhadas
- ✅ Restaurar com um clique
- ✅ Atualizar lista

## 💾 Economia de Espaço

### Exemplo Real:
```
Pasta Original: 1.5 GB (1000 arquivos)
Backup ZIP:     1.2 GB (20% economia)
Backup 7z:      850 MB (43% economia) ⭐
Backup TAR.GZ:  900 MB (40% economia)
```

### Backup Incremental:
```
1º Backup: 1000 arquivos (1.5 GB)
2º Backup: 10 arquivos modificados (15 MB) ⚡
3º Backup: 5 arquivos modificados (8 MB) ⚡
```

## 🔍 Verificar Status

### Ver Backups Disponíveis
```bash
python backupmaster_cli.py list -d "D:/Backups"
```

Mostra:
- 📁 Nome do arquivo
- 📊 Tipo (Completo/Incremental)
- 🗜️ Formato
- 📦 Quantidade de arquivos
- 💾 Economia de espaço (%)
- 🕐 Data e hora

## 🧪 Testar o Sistema

```bash
# Ativar ambiente virtual
# Windows:
venv\Scripts\activate.bat

# Linux/Mac:
source venv/bin/activate

# Executar testes
python test_backupmaster.py
```

Testes incluem:
- ✅ Criação de backup
- ✅ Backup incremental
- ✅ Todos os formatos (ZIP, 7z, TAR.GZ, TAR.BZ2)
- ✅ Restauração
- ✅ Listagem

## 📊 Monitoramento

### Durante o Backup (GUI)
- Barra de progresso: 0% → 100%
- Status: "Analisando arquivos..." → "Comprimindo..." → "Concluído!"
- Notificação do sistema quando termina

### Durante o Backup (CLI)
- Spinner animado
- Barra de progresso colorida
- Mensagens de status
- Estatísticas finais

## ⚠️ Dicas Importantes

### ✅ Faça
- Use backup incremental para backups frequentes
- Teste restaurações periodicamente
- Mantenha backups em múltiplos locais
- Use 7z para máxima compressão
- Verifique espaço em disco regularmente

### ❌ Evite
- Interromper backup em andamento
- Modificar arquivo `.backupmaster_metadata.json`
- Fazer backup de arquivos temporários
- Usar backup completo para backups diários
- Esquecer de testar restaurações

## 🆘 Problemas Comuns

### "Python não encontrado"
```bash
# Instale Python 3.8+ de python.org
# Marque "Add to PATH" durante instalação
```

### "Módulo não encontrado"
```bash
# Ative ambiente virtual
venv\Scripts\activate.bat  # Windows
source venv/bin/activate   # Linux/Mac

# Reinstale dependências
pip install -r requirements.txt
```

### "Sem espaço em disco"
```bash
# Verifique espaço disponível
# Use backup incremental
# Escolha formato com melhor compressão (7z)
```

### Interface gráfica não abre
```bash
# Instale PyQt6
pip install PyQt6

# Execute manualmente para ver erros
python backupmaster_gui.py
```

## 📚 Documentação Completa

- **README.md** - Visão geral do projeto
- **GETTING_STARTED.md** - Instalação e primeiros passos
- **USAGE.md** - Guia completo de uso
- **EXAMPLES.md** - Exemplos práticos detalhados
- **PROJECT_SUMMARY.md** - Resumo técnico do projeto

## 🎯 Fluxo de Trabalho Recomendado

### Configuração Inicial (Uma vez)
1. Execute `install.bat` (Windows) ou `install.sh` (Linux/Mac)
2. Teste com `python test_backupmaster.py`
3. Crie primeiro backup usando a GUI

### Uso Diário
1. Execute `run_gui.bat` ou use CLI
2. Backup incremental automático
3. Verifique notificações

### Manutenção Semanal
1. Verifique lista de backups
2. Teste uma restauração
3. Limpe backups antigos se necessário

### Backup Mensal Completo
1. Faça backup completo (sem `-i`)
2. Verifique espaço em disco
3. Copie para HD externo/nuvem

## 🏆 Pronto para Usar!

O BackupMaster está instalado e pronto! 

**Comece agora:**
```bash
# Interface Gráfica
run_gui.bat

# Ou CLI
python backupmaster_cli.py info
```

---

**BackupMaster v1.0.0**
Sistema Profissional de Backup
Desenvolvido com ❤️ em Python
