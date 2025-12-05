# Sistema de Telemetria e Estatísticas

## 📊 Visão Geral

O BackupMaster implementa um sistema de telemetria para rastrear:
- **Terabytes backupeados** por todos os usuários
- **Número de usuários ativos**
- **Estatísticas de uso** (formatos, tipos de backup, etc.)

## 🎯 Objetivos

1. **Rastrear Uso Global**: Quantos TB foram backupeados no total
2. **Usuários Ativos**: Quantas pessoas estão usando o sistema
3. **Métricas de Sucesso**: Formatos mais usados, economia de espaço, etc.
4. **Dashboard Público**: Estatísticas agregadas e anonimizadas

## 📈 Como Funciona

### 1. Coleta Local
Cada vez que você faz um backup, o sistema registra:
- Tamanho original dos dados
- Tamanho comprimido
- Número de arquivos
- Formato usado
- Tipo (completo/incremental)

Armazenado em: `~/.backupmaster_stats.json`

### 2. Estatísticas Pessoais
Você pode ver suas estatísticas a qualquer momento:

```bash
# Via CLI
python backupmaster_cli.py stats

# Via script
python stats_collector.py show
```

Mostra:
- Total de backups realizados
- Terabytes backupeados
- Espaço economizado
- Dias de uso
- Formatos preferidos

### 3. Estatísticas Globais (Opcional)
Para contribuir com estatísticas globais:

```bash
python stats_collector.py global
```

Isso:
- Coleta suas estatísticas (anonimizadas)
- Atualiza arquivo global
- Gera dashboard HTML

## 🔐 Privacidade

### O que é Coletado:
- ✅ Número total de backups
- ✅ Terabytes backupeados
- ✅ Formatos usados
- ✅ Timestamps (quando fez backup)

### O que NÃO é Coletado:
- ❌ Nomes de arquivos
- ❌ Conteúdo dos backups
- ❌ Caminhos de diretórios
- ❌ Dados pessoais além de nome/email
- ❌ Informações identificáveis

### Anonimização:
- Token do usuário é hasheado (SHA-256)
- Apenas primeiros 16 caracteres do hash são usados
- Impossível rastrear de volta ao usuário original

## 📊 Estatísticas Disponíveis

### Pessoais (Local)
```json
{
  "total_backups": 150,
  "total_bytes_original": 5497558138880,  // ~5 TB
  "total_bytes_compressed": 3298534883328,  // ~3 TB
  "total_files": 45000,
  "backups_by_format": {
    "zip": 30,
    "7z": 100,
    "tar.gz": 15,
    "tar.bz2": 5
  },
  "incremental_backups": 120,
  "full_backups": 30,
  "first_backup": "2025-01-01T10:00:00",
  "last_backup": "2025-12-05T13:00:00"
}
```

### Globais (Agregadas)
```json
{
  "total_users": 1250,
  "active_users_30d": 890,
  "total_backups": 187500,
  "total_terabytes": 6250.50,
  "last_update": "2025-12-05T13:00:00"
}
```

## 🌐 Dashboard Público

### Gerar Dashboard:
```bash
python stats_collector.py global
```

Cria arquivo `dashboard.html` com:
- Total de usuários
- Usuários ativos (últimos 30 dias)
- Total de backups realizados
- Terabytes backupeados

### Publicar Dashboard:
1. **GitHub Pages**:
   ```bash
   # Copie dashboard.html para repositório gh-pages
   git checkout gh-pages
   cp dashboard.html index.html
   git add index.html
   git commit -m "Update stats"
   git push
   ```

2. **Netlify/Vercel**:
   - Faça upload do dashboard.html
   - Configure para atualizar automaticamente

3. **Servidor Próprio**:
   - Hospede dashboard.html em qualquer servidor web

## 📝 Comandos

### Ver Estatísticas Pessoais
```bash
# Via CLI
python backupmaster_cli.py stats

# Via script
python stats_collector.py show
```

### Atualizar Estatísticas Globais
```bash
python stats_collector.py global
```

### Resetar Estatísticas
```bash
# Remova o arquivo
rm ~/.backupmaster_stats.json  # Linux/Mac
del %USERPROFILE%\.backupmaster_stats.json  # Windows
```

## 🔧 Implementação Técnica

### Arquivo de Estatísticas
**Local**: `~/.backupmaster_stats.json`

Atualizado automaticamente após cada backup.

### Coleta Automática
```python
# Em backupmaster/core.py
def create_backup(...):
    # ... código de backup ...
    
    # Registra telemetria
    self.telemetry.record_backup(backup_info)
```

### Agregação Global
```python
from backupmaster.telemetry import GlobalStatsCollector

collector = GlobalStatsCollector()
collector.add_user_stats(user_token, user_stats)
global_stats = collector.get_global_stats()
```

## 📊 Exemplo de Dashboard

O dashboard HTML gerado mostra:

```
┌─────────────────────────────────────────┐
│     🔄 BackupMaster                     │
│  Estatísticas Globais de Uso            │
├─────────────────────────────────────────┤
│                                         │
│  Total de Usuários:        1,250        │
│  Usuários Ativos (30d):      890        │
│  Total de Backups:       187,500        │
│  Terabytes Backupeados:  6,250.50 TB    │
│                                         │
│  Última atualização: 2025-12-05         │
└─────────────────────────────────────────┘
```

## 🚀 Automação

### Coletar Estatísticas Automaticamente

#### Windows (Task Scheduler):
```batch
# Crie tarefa agendada
# Programa: python.exe
# Argumentos: stats_collector.py global
# Frequência: Diária
```

#### Linux/Mac (Cron):
```bash
# Adicione ao crontab
0 0 * * * cd /caminho/para/backupmaster && python stats_collector.py global
```

### Webhook para Servidor
```python
# Em backupmaster/telemetry.py
def _send_telemetry(self):
    telemetry_data = {
        "total_backups": self.stats["total_backups"],
        "total_tb": round(self.stats["total_bytes_original"] / (1024**4), 2),
        "timestamp": datetime.now().isoformat()
    }
    
    # Envie para seu servidor
    requests.post(
        "https://seu-servidor.com/api/stats",
        json=telemetry_data
    )
```

## 📈 Métricas Rastreadas

### Por Usuário:
- Total de backups
- Terabytes backupeados
- Arquivos backupeados
- Formatos preferidos
- Tipos de backup (completo/incremental)
- Economia de espaço
- Dias de uso

### Globais:
- Total de usuários
- Usuários ativos (30 dias)
- Total de backups (todos os usuários)
- Terabytes totais backupeados
- Distribuição de formatos

## 🎯 Casos de Uso

### 1. Mostrar Impacto
```
"Mais de 6.250 TB de dados protegidos por 1.250 usuários!"
```

### 2. Marketing
```
"Junte-se a 890 usuários ativos que confiam no BackupMaster"
```

### 3. Desenvolvimento
- Identificar formatos mais usados
- Priorizar melhorias
- Entender padrões de uso

## 🔒 Segurança e Privacidade

### Dados Locais:
- Armazenados apenas na sua máquina
- Você controla quando/se compartilhar
- Pode ser deletado a qualquer momento

### Dados Globais:
- Completamente anonimizados
- Apenas agregados
- Sem informações identificáveis
- Opt-in (você escolhe compartilhar)

## ❓ FAQ

### Como vejo minhas estatísticas?
```bash
python backupmaster_cli.py stats
```

### Como contribuo para estatísticas globais?
```bash
python stats_collector.py global
```

### Posso desativar telemetria?
Sim! Basta não executar `stats_collector.py global`. As estatísticas locais são mantidas apenas para seu uso.

### Meus dados são enviados automaticamente?
Não! Você precisa executar manualmente `stats_collector.py global` para contribuir.

### Posso ver o código?
Sim! Todo código está em `backupmaster/telemetry.py` e é open source.

## 📞 Suporte

Dúvidas sobre telemetria?
- Leia o código: `backupmaster/telemetry.py`
- Execute: `python stats_collector.py help`
- Veja suas stats: `python backupmaster_cli.py stats`

---

**BackupMaster v1.0.0**
Sistema de Telemetria Transparente e Respeitoso
