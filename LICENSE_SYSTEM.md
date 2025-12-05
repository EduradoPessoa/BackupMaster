# Sistema de Licenciamento do BackupMaster

## 🔒 Visão Geral

O BackupMaster é **100% GRATUITO**, mas implementa um sistema de licenciamento para:
- Rastrear quantos usuários estão usando o sistema
- Entender em quais organizações está sendo utilizado
- Coletar feedback e melhorar o produto
- Manter estatísticas de uso

## 🎯 Como Funciona

### 1. Primeiro Uso
Quando você executa o BackupMaster pela primeira vez, será solicitado:
- **Nome**: Seu nome completo
- **Email**: Seu endereço de email
- **Organização**: (Opcional) Empresa ou projeto

### 2. Geração de Token
O sistema gera automaticamente:
- **Token único**: Hash SHA-256 baseado em seus dados
- **Machine ID**: Identificador único da máquina
- **Timestamp**: Data e hora do registro

### 3. Armazenamento
As informações são salvas em:
```
~/.backupmaster_license
```

Exemplo de conteúdo:
```json
{
  "token": "a1b2c3d4e5f6...",
  "name": "João Silva",
  "email": "joao@email.com",
  "organization": "Minha Empresa",
  "machine_id": "abc123def456",
  "registered_at": "2025-12-05T13:00:00",
  "last_validation": "2025-12-05T13:00:00",
  "version": "1.0.0"
}
```

### 4. Validação
A cada execução, o sistema:
1. Verifica se existe licença local
2. Valida estrutura dos dados
3. Atualiza timestamp de última validação
4. Permite uso do sistema

## 🌐 Validação Online vs Offline

### Modo Offline (Padrão)
- Valida apenas localmente
- Não requer internet
- Sempre funciona
- Usado por padrão

### Modo Online (Futuro)
- Pode validar contra servidor
- Verifica tokens banidos
- Coleta estatísticas de uso
- Opcional e não obrigatório

## 📊 Dados Coletados

### Informações Armazenadas:
- ✅ Nome do usuário
- ✅ Email
- ✅ Organização (opcional)
- ✅ Token único
- ✅ ID da máquina
- ✅ Data de registro
- ✅ Última validação
- ✅ Versão do software

### Informações NÃO Coletadas:
- ❌ Arquivos que você faz backup
- ❌ Conteúdo dos backups
- ❌ Localização dos arquivos
- ❌ Dados pessoais além do nome/email
- ❌ Histórico de navegação
- ❌ Qualquer informação sensível

## 🔐 Privacidade e Segurança

### Compromissos:
1. **Dados Mínimos**: Coletamos apenas o necessário
2. **Uso Local**: Licença armazenada apenas na sua máquina
3. **Sem Telemetria**: Não enviamos dados de uso
4. **Código Aberto**: Todo código é auditável
5. **Sem Tracking**: Não rastreamos atividades

### Arquivo de Licença:
- Armazenado em: `~/.backupmaster_license`
- Formato: JSON legível
- Pode ser visualizado a qualquer momento
- Pode ser removido manualmente

## 💻 Comandos

### Ver Informações da Licença
```bash
python backupmaster_cli.py license
```

Mostra:
- Nome do usuário
- Email
- Organização
- Data de registro
- Dias de uso
- Versão

### Remover Licença
```bash
# Simplesmente delete o arquivo
rm ~/.backupmaster_license  # Linux/Mac
del %USERPROFILE%\.backupmaster_license  # Windows
```

## 🛠️ Implementação Técnica

### Geração de Token
```python
# Token = SHA256(email + nome + UUID)
unique_data = f"{email}-{name}-{uuid.uuid4()}"
token = hashlib.sha256(unique_data.encode()).hexdigest()
```

### Machine ID
```python
# ID = SHA256(hostname + machine + node)[:16]
machine_info = f"{platform.node()}-{platform.machine()}-{socket.gethostname()}"
machine_id = hashlib.sha256(machine_info.encode()).hexdigest()[:16]
```

### Validação
```python
# Verifica campos obrigatórios
required_fields = ["token", "name", "email", "registered_at"]
for field in required_fields:
    if field not in user_data:
        return False
```

## 📝 Registro Manual

Se preferir, você pode criar o arquivo manualmente:

```bash
# Linux/Mac
cat > ~/.backupmaster_license << EOF
{
  "token": "seu_token_aqui",
  "name": "Seu Nome",
  "email": "seu@email.com",
  "organization": "Sua Empresa",
  "machine_id": "abc123",
  "registered_at": "2025-12-05T13:00:00",
  "last_validation": "2025-12-05T13:00:00",
  "version": "1.0.0"
}
EOF
```

## 🔄 Transferência de Licença

### Usar em Outra Máquina
1. Copie o arquivo `.backupmaster_license`
2. Cole na pasta home da nova máquina
3. O sistema reconhecerá automaticamente

### Múltiplas Máquinas
- Você pode usar a mesma licença em várias máquinas
- Cada máquina terá seu próprio Machine ID
- Não há limite de instalações

## 🚫 Revogação de Licença

### Quando Necessário:
- Trocar de email
- Atualizar informações
- Resolver problemas

### Como Fazer:
```bash
# Remova o arquivo de licença
rm ~/.backupmaster_license

# Na próxima execução, será solicitado novo registro
python backupmaster_cli.py backup ...
```

## 📈 Estatísticas (Futuro)

### Planejado:
- Dashboard público com estatísticas agregadas
- Número total de usuários
- Países/regiões de uso
- Versões mais utilizadas
- Formatos de compressão preferidos

### Sempre Anônimo:
- Dados agregados apenas
- Sem identificação individual
- Opt-in para compartilhamento
- Transparência total

## ❓ FAQ

### Por que preciso me registrar?
Para nos ajudar a entender quem está usando o BackupMaster e melhorar o produto.

### É realmente gratuito?
Sim! 100% gratuito, sem limitações, para sempre.

### Posso usar em empresa?
Sim! Sem restrições comerciais.

### Meus dados estão seguros?
Sim! Armazenados apenas localmente, sem envio para servidores.

### Posso ver o código?
Sim! Todo código é open source e auditável.

### Posso remover a licença?
Sim! Basta deletar o arquivo `.backupmaster_license`.

### Funciona offline?
Sim! Não requer internet para funcionar.

### Quantas máquinas posso usar?
Ilimitadas! Use em quantas máquinas quiser.

## 🔧 Desenvolvimento

### Desabilitar Licenciamento (Dev)
```python
# Em backupmaster/auth.py, modifique:
def validate_license(self, offline_mode: bool = False) -> bool:
    return True  # Sempre válido para desenvolvimento
```

### Testar Registro
```python
from backupmaster.auth import LicenseManager

lm = LicenseManager()
result = lm.register_user("Teste", "teste@email.com", "Dev")
print(result)
```

### Ver Licença
```python
from backupmaster.auth import show_license_info
show_license_info()
```

## 📞 Suporte

Problemas com licenciamento?
- Verifique o arquivo `~/.backupmaster_license`
- Execute `python backupmaster_cli.py license`
- Remova e registre novamente se necessário

## 🎯 Conclusão

O sistema de licenciamento do BackupMaster é:
- ✅ **Simples**: Registro em 3 campos
- ✅ **Rápido**: Menos de 30 segundos
- ✅ **Seguro**: Dados apenas locais
- ✅ **Transparente**: Código aberto
- ✅ **Gratuito**: Sem custos, sempre

Obrigado por usar o BackupMaster! 🎉
