# 🐛 BackupMaster - Troubleshooting

## Problema Reportado: Aplicação Fecha ao Confirmar Agendamento

### 🔍 Possíveis Causas

#### 1. **Erro de Validação**
- Campos obrigatórios não preenchidos
- Caminho de pasta inválido
- Formato de horário incorreto

#### 2. **Erro de Permissão**
- Sem permissão para criar arquivo `~/.backupmaster_schedules.json`
- Pasta de destino sem permissão de escrita

#### 3. **Dependência Faltando**
- Biblioteca `schedule` não instalada

---

## ✅ Soluções

### **Solução 1: Verificar Campos Obrigatórios**

Ao criar agendamento, preencha **TODOS** os campos:

```
✅ Nome: "Backup Diário"
✅ Origem: C:\Users\Documents (pasta existente)
✅ Destino: D:\Backups (pasta existente)
✅ Formato: ZIP
✅ Frequência: Diário
✅ Horário: 02:00
✅ Ativo: Marcado
```

### **Solução 2: Instalar Dependências**

```bash
pip install schedule
```

### **Solução 3: Executar com Debug**

Use o script de debug para ver erros:

```bash
python debug_gui.py
```

Isso mostrará o erro completo antes de fechar.

### **Solução 4: Verificar Permissões**

#### Windows:
```powershell
# Verificar se pode criar arquivo
echo "test" > %USERPROFILE%\.backupmaster_test
del %USERPROFILE%\.backupmaster_test
```

#### Linux/macOS:
```bash
# Verificar permissões
touch ~/.backupmaster_test
rm ~/.backupmaster_test
```

---

## 🧪 Teste Passo a Passo

### **Teste 1: Criar Agendamento Simples**

1. **Abra** BackupMaster
2. **Clique** "📅 Gerenciar Agendamentos"
3. **Clique** "➕ Novo Agendamento"
4. **Preencha**:
   ```
   Nome: Teste
   Origem: C:\Windows\System32 (pasta que existe)
   Destino: C:\Temp (pasta que existe)
   Formato: ZIP
   Frequência: Diário
   Horário: 15:00
   Ativo: ✅
   ```
5. **Clique** "💾 Salvar"
6. **Aguarde** mensagem "Agendamento criado com sucesso!"
7. **Verifique** se aparece na lista

### **Teste 2: Verificar Arquivo Criado**

Após criar agendamento, verifique se o arquivo foi criado:

#### Windows:
```powershell
type %USERPROFILE%\.backupmaster_schedules.json
```

#### Linux/macOS:
```bash
cat ~/.backupmaster_schedules.json
```

**Deve mostrar**:
```json
[
  {
    "id": "abc123",
    "name": "Teste",
    "source": "C:\\Windows\\System32",
    ...
  }
]
```

---

## 🔧 Correções Aplicadas

### **Melhorias no Código**:

1. **Validação Melhorada**:
   - Verifica campos vazios
   - Valida caminhos de pasta
   - Mostra mensagens de erro claras

2. **Tratamento de Erros**:
   - Try/catch em operações críticas
   - Mensagens de erro detalhadas
   - Não fecha aplicação em caso de erro

3. **Debug Script**:
   - `debug_gui.py` captura todos os erros
   - Mostra traceback completo
   - Aguarda ENTER antes de fechar

---

## 📝 Logs de Erro

### **Onde Encontrar Logs**:

#### Windows:
```
%USERPROFILE%\.backupmaster_error.log
```

#### Linux/macOS:
```
~/.backupmaster_error.log
```

### **Como Ativar Logs** (futuro):

Adicione ao início de `backupmaster_gui.py`:

```python
import logging

logging.basicConfig(
    filename=os.path.expanduser('~/.backupmaster_error.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

---

## 🐛 Erros Comuns

### **Erro 1: ModuleNotFoundError: No module named 'schedule'**

**Solução**:
```bash
pip install schedule
```

### **Erro 2: PermissionError: [Errno 13] Permission denied**

**Solução**:
- Execute como administrador (Windows)
- Verifique permissões da pasta home

### **Erro 3: FileNotFoundError: [Errno 2] No such file or directory**

**Solução**:
- Verifique se pastas de origem/destino existem
- Use caminhos absolutos
- Crie pastas antes de agendar

### **Erro 4: KeyError: 'format'**

**Solução**:
- Selecione um formato no dropdown
- Não deixe campos vazios

---

## 🔄 Como Reportar Bug

Se o problema persistir, reporte com estas informações:

### **Template de Bug Report**:

```markdown
**Descrição**:
Aplicação fecha ao confirmar agendamento

**Passos para Reproduzir**:
1. Abrir BackupMaster
2. Clicar "Gerenciar Agendamentos"
3. Clicar "Novo Agendamento"
4. Preencher campos
5. Clicar "Salvar"
6. Aplicação fecha

**Dados Preenchidos**:
- Nome: [seu nome]
- Origem: [caminho]
- Destino: [caminho]
- Formato: [ZIP/TAR.GZ/etc]
- Frequência: [Diário/Semanal/Mensal]
- Horário: [HH:MM]

**Ambiente**:
- OS: Windows 10/11
- Python: 3.x
- Versão BackupMaster: 1.0.0

**Output do debug_gui.py**:
[Cole aqui o erro completo]

**Arquivo de Agendamentos**:
[Cole conteúdo de ~/.backupmaster_schedules.json se existir]
```

---

## ✅ Checklist de Verificação

Antes de reportar bug, verifique:

- [ ] Biblioteca `schedule` instalada
- [ ] Todos os campos preenchidos
- [ ] Pastas de origem/destino existem
- [ ] Permissão de escrita na pasta home
- [ ] Executou com `debug_gui.py`
- [ ] Verificou arquivo `.backupmaster_schedules.json`

---

## 🚀 Workaround Temporário

Se agendamento não funcionar, use alternativas:

### **Opção 1: Agendador do Windows**

```powershell
# Criar tarefa agendada
schtasks /create /tn "BackupMaster" /tr "python C:\path\to\backupmaster_cli.py backup C:\origem C:\destino" /sc daily /st 02:00
```

### **Opção 2: Cron (Linux/macOS)**

```bash
# Editar crontab
crontab -e

# Adicionar linha
0 2 * * * python3 /path/to/backupmaster_cli.py backup /origem /destino
```

### **Opção 3: Usar CLI Manualmente**

```bash
# Criar backup manual
python backupmaster_cli.py backup C:\origem C:\destino --format zip
```

---

**Se o problema persistir, execute com `debug_gui.py` e reporte o erro completo!** 🐛
