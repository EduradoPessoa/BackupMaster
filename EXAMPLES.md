# Exemplos de Uso do BackupMaster

Este arquivo contém exemplos práticos de como usar o BackupMaster.

## 📋 Índice

1. [Backup Simples](#backup-simples)
2. [Backup Incremental](#backup-incremental)
3. [Diferentes Formatos](#diferentes-formatos)
4. [Restauração](#restauração)
5. [Automação](#automação)

## Backup Simples

### Exemplo 1: Backup de Documentos em ZIP

```bash
python backupmaster_cli.py backup \
  --source "C:/Users/Usuario/Documentos" \
  --dest "D:/Backups" \
  --format zip
```

### Exemplo 2: Backup de Fotos em 7z (máxima compressão)

```bash
python backupmaster_cli.py backup \
  --source "C:/Users/Usuario/Fotos" \
  --dest "E:/Backups/Fotos" \
  --format 7z
```

## Backup Incremental

### Exemplo 3: Backup Incremental Diário

```bash
# Primeiro backup (completo)
python backupmaster_cli.py backup \
  --source "C:/Projetos" \
  --dest "D:/Backups/Projetos" \
  --format 7z \
  --incremental

# Backups seguintes (apenas arquivos modificados)
python backupmaster_cli.py backup \
  --source "C:/Projetos" \
  --dest "D:/Backups/Projetos" \
  --format 7z \
  --incremental
```

## Diferentes Formatos

### Exemplo 4: Comparação de Formatos

```bash
# ZIP - Rápido e compatível
python backupmaster_cli.py backup -s "C:/Dados" -d "D:/Backups" -f zip

# 7z - Máxima compressão
python backupmaster_cli.py backup -s "C:/Dados" -d "D:/Backups" -f 7z

# TAR.GZ - Padrão Linux
python backupmaster_cli.py backup -s "C:/Dados" -d "D:/Backups" -f tar.gz

# TAR.BZ2 - Alta compressão Unix
python backupmaster_cli.py backup -s "C:/Dados" -d "D:/Backups" -f tar.bz2
```

## Restauração

### Exemplo 5: Listar e Restaurar Backup

```bash
# Listar backups disponíveis
python backupmaster_cli.py list --dest "D:/Backups"

# Restaurar backup específico
python backupmaster_cli.py restore \
  --backup "D:/Backups/Documentos_full_20251205_140000.7z" \
  --dest "C:/Restaurar"
```

## Automação

### Exemplo 6: Script de Backup Automático (Windows)

Crie um arquivo `backup_automatico.bat`:

```batch
@echo off
REM Backup automático diário

REM Ativa ambiente virtual
call venv\Scripts\activate.bat

REM Backup incremental de documentos
python backupmaster_cli.py backup ^
  -s "C:/Users/Usuario/Documentos" ^
  -d "D:/Backups/Documentos" ^
  -f 7z ^
  -i

REM Backup incremental de projetos
python backupmaster_cli.py backup ^
  -s "C:/Projetos" ^
  -d "D:/Backups/Projetos" ^
  -f 7z ^
  -i

echo Backups concluídos!
pause
```

### Exemplo 7: Script de Backup Automático (Linux/Mac)

Crie um arquivo `backup_automatico.sh`:

```bash
#!/bin/bash
# Backup automático diário

# Ativa ambiente virtual
source venv/bin/activate

# Backup incremental de documentos
python backupmaster_cli.py backup \
  -s "/home/usuario/Documentos" \
  -d "/backup/Documentos" \
  -f 7z \
  -i

# Backup incremental de projetos
python backupmaster_cli.py backup \
  -s "/home/usuario/Projetos" \
  -d "/backup/Projetos" \
  -f 7z \
  -i

echo "Backups concluídos!"
```

Torne executável:
```bash
chmod +x backup_automatico.sh
```

### Exemplo 8: Agendamento no Windows (Task Scheduler)

1. Abra o Agendador de Tarefas
2. Crie nova tarefa básica
3. Nome: "Backup Diário"
4. Gatilho: Diariamente às 02:00
5. Ação: Iniciar programa
   - Programa: `C:\caminho\para\backup_automatico.bat`

### Exemplo 9: Agendamento no Linux (Cron)

```bash
# Editar crontab
crontab -e

# Adicionar linha para backup diário às 2h
0 2 * * * /caminho/para/backup_automatico.sh >> /var/log/backup.log 2>&1
```

## Casos de Uso Avançados

### Exemplo 10: Backup com Nome Customizado

```bash
python backupmaster_cli.py backup \
  --source "C:/Projeto/MeuApp" \
  --dest "D:/Backups" \
  --format 7z \
  --name "meuapp_v1.0"
```

### Exemplo 11: Múltiplos Backups em Sequência

```bash
# Backup de diferentes pastas
python backupmaster_cli.py backup -s "C:/Documentos" -d "D:/Backups" -f 7z -i
python backupmaster_cli.py backup -s "C:/Fotos" -d "D:/Backups" -f 7z -i
python backupmaster_cli.py backup -s "C:/Videos" -d "D:/Backups" -f 7z -i
python backupmaster_cli.py backup -s "C:/Musicas" -d "D:/Backups" -f zip -i
```

### Exemplo 12: Backup para Múltiplos Destinos

```bash
# Backup local
python backupmaster_cli.py backup \
  -s "C:/Dados" \
  -d "D:/Backups" \
  -f 7z -i

# Backup para HD externo
python backupmaster_cli.py backup \
  -s "C:/Dados" \
  -d "E:/Backups" \
  -f 7z -i

# Backup para rede
python backupmaster_cli.py backup \
  -s "C:/Dados" \
  -d "\\servidor\backups" \
  -f 7z -i
```

## Dicas de Uso

### ✅ Boas Práticas

1. **Use backup incremental para backups frequentes**
   - Economiza tempo e espaço
   - Ideal para backups diários

2. **Escolha o formato adequado**
   - ZIP: Compatibilidade e velocidade
   - 7z: Máxima compressão
   - TAR.GZ/BZ2: Ambientes Linux

3. **Mantenha múltiplas cópias**
   - Regra 3-2-1: 3 cópias, 2 mídias diferentes, 1 offsite

4. **Teste suas restaurações**
   - Periodicamente restaure backups para verificar integridade

5. **Monitore o espaço em disco**
   - Verifique regularmente o espaço disponível

### ⚠️ Avisos

- Não interrompa um backup em andamento
- Certifique-se de ter espaço suficiente no destino
- Mantenha backups importantes em local seguro
- Não modifique o arquivo `.backupmaster_metadata.json`

## Suporte

Para mais informações:
- README.md - Visão geral
- USAGE.md - Guia completo
- GitHub Issues - Reportar problemas
