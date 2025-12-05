# BackupMaster 🔄

**Sistema Profissional de Backup**

![BackupMaster](https://img.shields.io/badge/version-1.0.0-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Mac-blue)

## 🌟 Características

### Backup Inteligente
Sistema incremental que só copia arquivos modificados, economizando tempo e espaço

### Multi-Plataforma
Funciona no Windows, Linux e Mac. Interface desktop e web disponível

### 100% Gratuito
Software livre e open source. Use sem limitações em empresas e projetos pessoais

### 🔒 Registro Simples
Requer registro gratuito para rastreamento de usuários (nome e email). Seus dados ficam apenas na sua máquina.

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/backupmaster.git
cd backupmaster

# Instale as dependências
pip install -r requirements.txt
```

## 💻 Uso

### Interface Gráfica (GUI)
```bash
python backupmaster_gui.py
```

### Interface de Linha de Comando (CLI)
```bash
# Criar um backup
python backupmaster_cli.py backup --source "C:/Documentos" --dest "D:/Backups" --format 7z

# Listar backups
python backupmaster_cli.py list --dest "D:/Backups"

# Restaurar backup
python backupmaster_cli.py restore --backup "backup_2025-12-05.7z" --dest "C:/Restaurar"

# Backup incremental
python backupmaster_cli.py backup --source "C:/Documentos" --dest "D:/Backups" --incremental
```

## 📦 Formatos de Compressão Suportados

- **ZIP** - Compatibilidade universal
- **7z** - Máxima compressão
- **TAR.GZ** - Padrão Linux/Unix
- **TAR.BZ2** - Alta compressão

## 🔧 Recursos

- ✅ Backup incremental (apenas arquivos modificados)
- ✅ Múltiplos formatos de compressão
- ✅ Interface gráfica intuitiva
- ✅ System tray no Windows
- ✅ Agendamento de backups
- ✅ Histórico de backups
- ✅ Estatísticas de economia de espaço
- ✅ Barra de progresso em tempo real
- ✅ Notificações do sistema

## 🔒 Sistema de Licenciamento

O BackupMaster é **100% GRATUITO**, mas requer registro para rastreamento de usuários.

### Primeiro Uso
No primeiro uso, você será solicitado a fornecer:
- Nome
- Email  
- Organização (opcional)

### Privacidade
- ✅ Dados armazenados apenas localmente
- ✅ Nenhuma informação enviada para servidores
- ✅ Código aberto e auditável
- ✅ Sem telemetria ou tracking

### Comandos
```bash
# Ver informações da licença
python backupmaster_cli.py license

# Remover licença (para re-registro)
# Windows: del %USERPROFILE%\.backupmaster_license
# Linux/Mac: rm ~/.backupmaster_license
```

Leia mais em: [LICENSE_SYSTEM.md](LICENSE_SYSTEM.md)

## 📊 Telemetria e Estatísticas

O BackupMaster rastreia estatísticas de uso para mostrar o impacto global:

### Estatísticas Pessoais
```bash
# Ver suas estatísticas
python backupmaster_cli.py stats
```

Mostra:
- Terabytes backupeados
- Número de backups
- Espaço economizado
- Formatos preferidos

### Estatísticas Globais (Opcional)
```bash
# Contribuir para estatísticas globais
python stats_collector.py global
```

Gera dashboard com:
- Total de usuários
- Usuários ativos (30 dias)
- Terabytes totais backupeados
- Total de backups realizados

**Privacidade**: Dados completamente anonimizados. Leia mais em: [TELEMETRY.md](TELEMETRY.md)

## 📚 Documentação

- [GETTING_STARTED.md](GETTING_STARTED.md) - Instalação e primeiros passos
- [QUICK_START.md](QUICK_START.md) - Guia rápido de referência
- [USAGE.md](USAGE.md) - Guia completo de uso
- [EXAMPLES.md](EXAMPLES.md) - Exemplos práticos
- [LICENSE_SYSTEM.md](LICENSE_SYSTEM.md) - Sistema de licenciamento
- [GITHUB_SETUP.md](GITHUB_SETUP.md) - Publicar no GitHub

## 📄 Licença

MIT License - Use livremente!
