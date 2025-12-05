# 🧪 BackupMaster - Ambiente de QA

## 📋 Informações da Branch QA

### **Branch Criada**: `qa`
- **Origem**: `main`
- **Data**: 2025-12-05
- **Commit**: Todos os fontes da master incluídos
- **Status**: Pronta para testes

### **Acesso ao Repositório**:
```bash
# Clone do repositório
git clone https://github.com/EduradoPessoa/BackupMaster.git

# Mudar para branch QA
cd BackupMaster
git checkout qa
```

---

## 🔐 Credenciais de Acesso

### **Dashboard de Telemetria - Admin**

#### **URL Local**:
```
http://localhost:8000
```

#### **Senha de Admin**:
```
backupmaster2025
```

#### **Como Acessar**:
1. Abra o dashboard
2. Clique no botão "Admin" (canto superior direito)
3. Digite a senha: `backupmaster2025`
4. Clique em "Entrar"

#### **Funcionalidades Admin**:
- ✅ Ver lista completa de usuários
- ✅ Ver emails e tokens
- ✅ Ver estatísticas individuais (backups, TB)
- ✅ Buscar usuários
- ✅ Copiar tokens
- ✅ Ver último acesso

---

## 🚀 Como Executar para Testes

### **1. Instalar Dependências**

#### Windows:
```bash
# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

#### Linux/macOS:
```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### **2. Executar Aplicação GUI**

```bash
python backupmaster_gui.py
```

**Funcionalidades para Testar**:
- ✅ Registro de usuário (primeira execução)
- ✅ Criar backup (ZIP, TAR.GZ, TAR.BZ2)
- ✅ Backup incremental
- ✅ Restaurar backup
- ✅ Histórico de backups
- ✅ Agendamento de backups
- ✅ System tray
- ✅ Notificações

### **3. Executar Aplicação CLI**

```bash
# Ver comandos disponíveis
python backupmaster_cli.py --help

# Criar backup
python backupmaster_cli.py backup C:\origem C:\destino

# Listar backups
python backupmaster_cli.py list C:\destino

# Ver estatísticas
python backupmaster_cli.py stats

# Ver licença
python backupmaster_cli.py license
```

### **4. Executar Dashboard de Telemetria**

```bash
# Iniciar servidor
python serve_dashboard.py

# Acessar no navegador
http://localhost:8000
```

**Funcionalidades para Testar**:
- ✅ Visualização de estatísticas públicas
- ✅ Gráficos de downloads
- ✅ Gráficos de formatos
- ✅ Login admin (senha: `backupmaster2025`)
- ✅ Painel administrativo
- ✅ Busca de usuários
- ✅ Downloads (Windows, Linux, macOS)
- ✅ Compartilhamento social
- ✅ Convite por email

---

## 🧪 Casos de Teste

### **TC001 - Registro de Usuário**
1. Execute `python backupmaster_gui.py`
2. Preencha nome, email e organização
3. Clique em "OK"
4. **Esperado**: Mensagem de sucesso com token

### **TC002 - Criar Backup ZIP**
1. Selecione pasta de origem
2. Selecione pasta de destino
3. Formato: ZIP
4. Clique "Iniciar Backup"
5. **Esperado**: Barra de progresso, backup criado, aparece no histórico

### **TC003 - Backup Incremental**
1. Crie um backup completo
2. Modifique alguns arquivos na origem
3. Marque "Backup Incremental"
4. Crie novo backup
5. **Esperado**: Apenas arquivos modificados são copiados

### **TC004 - Restaurar Backup**
1. Selecione backup no histórico
2. Clique "Restaurar Selecionado"
3. Escolha pasta de destino
4. Confirme
5. **Esperado**: Arquivos restaurados na pasta escolhida

### **TC005 - Agendamento de Backup**
1. Clique "Gerenciar Agendamentos"
2. Clique "Novo Agendamento"
3. Preencha dados
4. Salve
5. **Esperado**: Agendamento aparece na lista

### **TC006 - Dashboard - Visualização Pública**
1. Acesse http://localhost:8000
2. Veja estatísticas
3. **Esperado**: Cards animados, gráficos funcionando

### **TC007 - Dashboard - Login Admin**
1. Clique "Admin"
2. Digite senha: `backupmaster2025`
3. Clique "Entrar"
4. **Esperado**: Painel admin aparece com lista de usuários

### **TC008 - Dashboard - Busca de Usuários**
1. Faça login como admin
2. Digite nome/email na busca
3. **Esperado**: Lista filtrada em tempo real

### **TC009 - Dashboard - Download**
1. Clique em botão de download (Windows/Linux/macOS)
2. **Esperado**: Download iniciado, rastreado no banco

### **TC010 - Dashboard - Compartilhamento**
1. Clique em botão de compartilhamento
2. **Esperado**: Abre rede social com mensagem pré-formatada

---

## 🐛 Reportar Bugs

### **Template de Bug**:
```
Título: [Componente] Descrição curta

Descrição:
- O que aconteceu
- O que era esperado

Passos para Reproduzir:
1. Passo 1
2. Passo 2
3. Passo 3

Ambiente:
- OS: Windows 10/11, Linux, macOS
- Python: 3.x
- Branch: qa

Screenshots:
[Se aplicável]
```

### **Onde Reportar**:
- GitHub Issues: https://github.com/EduradoPessoa/BackupMaster/issues
- Label: `bug`, `qa`

---

## ✅ Checklist de QA

### **Funcionalidades Principais**:
- [ ] Registro de usuário funciona
- [ ] Backup ZIP funciona
- [ ] Backup TAR.GZ funciona
- [ ] Backup TAR.BZ2 funciona
- [ ] Backup incremental funciona
- [ ] Restauração funciona
- [ ] Histórico de backups aparece
- [ ] System tray funciona
- [ ] Notificações aparecem

### **Agendamento**:
- [ ] Criar agendamento funciona
- [ ] Editar agendamento funciona
- [ ] Excluir agendamento funciona
- [ ] Agendamento executa no horário
- [ ] Notificação de backup agendado aparece

### **Dashboard**:
- [ ] Estatísticas carregam
- [ ] Gráficos animam
- [ ] Login admin funciona
- [ ] Painel admin aparece
- [ ] Busca funciona
- [ ] Downloads funcionam
- [ ] Compartilhamento funciona
- [ ] Convite por email funciona

### **CLI**:
- [ ] Comando `backup` funciona
- [ ] Comando `list` funciona
- [ ] Comando `restore` funciona
- [ ] Comando `stats` funciona
- [ ] Comando `license` funciona

---

## 📊 Banco de Dados de Teste

### **MySQL (Opcional)**:
Se quiser testar com banco real:

1. **Importe** `web/database.sql`
2. **Configure** `web/api/config.php`
3. **Teste** API: `http://localhost/api/telemetry.php?type=public`

### **Dados de Exemplo**:
O script SQL já inclui:
- 3 usuários de exemplo
- Estatísticas de teste
- Downloads de exemplo

---

## 🔄 Atualizar Branch QA

Quando houver novos commits na `main`:

```bash
# Mudar para main
git checkout main

# Atualizar main
git pull origin main

# Mudar para qa
git checkout qa

# Merge da main
git merge main

# Push
git push origin qa
```

---

## 📞 Contato

**Dúvidas sobre testes?**
- Abra uma issue no GitHub
- Label: `question`, `qa`

---

## ✅ Status da Branch QA

```
Branch: qa
Commits: Sincronizada com main
Status: ✅ Pronta para testes
Última atualização: 2025-12-05
```

---

**Boa sorte nos testes! 🚀**
