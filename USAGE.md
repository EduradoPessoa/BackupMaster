# Guia de Uso do BackupMaster

## 🚀 Início Rápido

### Instalação

#### Windows
```bash
install.bat
```

#### Linux/Mac
```bash
chmod +x install.sh
./install.sh
```

## 💻 Interface Gráfica (GUI)

### Iniciar a GUI

#### Windows
```bash
run_gui.bat
```

#### Linux/Mac
```bash
./run_gui.sh
```

### Recursos da GUI

1. **Criar Backup**
   - Selecione o diretório de origem (📁 Origem)
   - Selecione o diretório de destino (💾 Destino)
   - Escolha o formato de compressão (ZIP, 7z, TAR.GZ, TAR.BZ2)
   - Marque "Backup Incremental" se quiser copiar apenas arquivos modificados
   - Clique em "🚀 Iniciar Backup"

2. **Acompanhar Progresso**
   - A barra de progresso mostra o andamento em tempo real
   - O status mostra qual arquivo está sendo processado

3. **Visualizar Histórico**
   - A tabela mostra todos os backups realizados
   - Informações: nome do arquivo, tipo, formato, quantidade de arquivos e economia de espaço

4. **Restaurar Backup**
   - Selecione um backup na tabela
   - Clique em "📥 Restaurar Selecionado"
   - Escolha o diretório de destino
   - Confirme a restauração

5. **System Tray**
   - O aplicativo fica na bandeja do sistema (system tray)
   - Clique com botão direito no ícone para acessar o menu
   - Duplo clique para mostrar/ocultar a janela
   - Receba notificações quando backups forem concluídos

## 🖥️ Interface de Linha de Comando (CLI)

### Comandos Disponíveis

#### 1. Criar Backup

**Backup Completo em ZIP:**
```bash
python backupmaster_cli.py backup -s "C:/Documentos" -d "D:/Backups" -f zip
```

**Backup Incremental em 7z:**
```bash
python backupmaster_cli.py backup -s "C:/Documentos" -d "D:/Backups" -f 7z -i
```

**Backup com Nome Customizado:**
```bash
python backupmaster_cli.py backup -s "C:/Documentos" -d "D:/Backups" -f zip -n "meu_backup"
```

**Parâmetros:**
- `-s, --source`: Diretório de origem (obrigatório)
- `-d, --dest`: Diretório de destino (obrigatório)
- `-f, --format`: Formato de compressão (zip, 7z, tar.gz, tar.bz2)
- `-i, --incremental`: Ativa backup incremental
- `-n, --name`: Nome customizado do backup

#### 2. Listar Backups

```bash
python backupmaster_cli.py list -d "D:/Backups"
```

Mostra uma tabela com todos os backups disponíveis, incluindo:
- Nome do arquivo
- Tipo (Completo ou Incremental)
- Formato de compressão
- Quantidade de arquivos
- Economia de espaço (%)
- Data e hora

#### 3. Restaurar Backup

```bash
python backupmaster_cli.py restore -b "D:/Backups/backup.7z" -d "C:/Restaurar"
```

**Parâmetros:**
- `-b, --backup`: Caminho do arquivo de backup (obrigatório)
- `-d, --dest`: Diretório de destino para restauração (obrigatório)

#### 4. Informações

```bash
python backupmaster_cli.py info
```

Mostra informações sobre o BackupMaster, características e exemplos de uso.

## 📦 Formatos de Compressão

### ZIP
- **Vantagens**: Compatibilidade universal, rápido
- **Uso recomendado**: Backups que precisam ser acessados em qualquer sistema
- **Compressão**: Média

### 7z
- **Vantagens**: Máxima compressão, economia de espaço
- **Uso recomendado**: Backups de longo prazo, arquivos grandes
- **Compressão**: Excelente

### TAR.GZ
- **Vantagens**: Padrão em sistemas Linux/Unix, boa compressão
- **Uso recomendado**: Ambientes Linux, servidores
- **Compressão**: Boa

### TAR.BZ2
- **Vantagens**: Alta compressão, padrão Unix
- **Uso recomendado**: Backups de longo prazo em Linux
- **Compressão**: Muito boa

## 🔄 Backup Incremental

O backup incremental é uma funcionalidade inteligente que:

1. **Primeira execução**: Copia todos os arquivos (backup completo)
2. **Execuções seguintes**: Copia apenas arquivos que foram:
   - Criados desde o último backup
   - Modificados desde o último backup

### Vantagens
- ⚡ Muito mais rápido
- 💾 Economiza espaço em disco
- 🔋 Usa menos recursos do sistema

### Como funciona
O BackupMaster calcula um hash MD5 de cada arquivo e armazena em um arquivo de metadados (`.backupmaster_metadata.json`). Nas próximas execuções, compara os hashes para identificar mudanças.

## 📊 Exemplos Práticos

### Exemplo 1: Backup Diário de Documentos

```bash
# Primeiro backup (completo)
python backupmaster_cli.py backup -s "C:/Users/Usuario/Documentos" -d "D:/Backups/Documentos" -f 7z

# Backups seguintes (incrementais)
python backupmaster_cli.py backup -s "C:/Users/Usuario/Documentos" -d "D:/Backups/Documentos" -f 7z -i
```

### Exemplo 2: Backup de Projeto de Desenvolvimento

```bash
# Backup incremental em ZIP para facilitar acesso
python backupmaster_cli.py backup -s "C:/Projetos/MeuApp" -d "D:/Backups/Projetos" -f zip -i -n "meuapp_dev"
```

### Exemplo 3: Backup de Fotos

```bash
# Backup completo em 7z para máxima compressão
python backupmaster_cli.py backup -s "C:/Users/Usuario/Fotos" -d "E:/Backups/Fotos" -f 7z
```

### Exemplo 4: Restauração de Backup

```bash
# Listar backups disponíveis
python backupmaster_cli.py list -d "D:/Backups"

# Restaurar backup específico
python backupmaster_cli.py restore -b "D:/Backups/backup_20251205_143000.7z" -d "C:/Restaurar"
```

## 🛠️ Agendamento de Backups

### Windows (Task Scheduler)

1. Abra o Agendador de Tarefas
2. Crie uma nova tarefa
3. Configure o gatilho (diário, semanal, etc.)
4. Ação: Iniciar programa
   - Programa: `C:\caminho\para\venv\Scripts\python.exe`
   - Argumentos: `backupmaster_cli.py backup -s "C:/Documentos" -d "D:/Backups" -f 7z -i`
   - Iniciar em: `C:\caminho\para\backupmaster`

### Linux/Mac (Cron)

```bash
# Editar crontab
crontab -e

# Adicionar linha para backup diário às 2h da manhã
0 2 * * * cd /caminho/para/backupmaster && ./venv/bin/python backupmaster_cli.py backup -s "/home/usuario/documentos" -d "/backup" -f 7z -i
```

## 🔍 Solução de Problemas

### Erro: "Módulo não encontrado"
```bash
# Certifique-se de que o ambiente virtual está ativado
# Windows
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate

# Reinstale as dependências
pip install -r requirements.txt
```

### Erro: "Permissão negada"
```bash
# Linux/Mac - dê permissão de execução aos scripts
chmod +x install.sh run_gui.sh run_cli.sh
```

### Backup muito lento
- Use backup incremental (`-i`)
- Escolha formato ZIP para velocidade
- Exclua arquivos temporários da origem

### Erro ao restaurar
- Verifique se o arquivo de backup não está corrompido
- Certifique-se de ter espaço suficiente no destino
- Verifique permissões de escrita no diretório de destino

## 📞 Suporte

Para mais informações, consulte:
- README.md - Visão geral do projeto
- LICENSE - Termos de uso
- GitHub Issues - Reportar problemas

## 🎯 Dicas e Boas Práticas

1. **Teste seus backups**: Sempre teste a restauração periodicamente
2. **Múltiplos destinos**: Mantenha backups em diferentes locais (HD externo, nuvem)
3. **Backup incremental**: Use para backups frequentes (diários)
4. **Backup completo**: Faça semanalmente ou mensalmente
5. **Monitore o espaço**: Verifique regularmente o espaço em disco
6. **Documentação**: Mantenha registro de quais backups contêm o quê
7. **Segurança**: Armazene backups importantes em local seguro
