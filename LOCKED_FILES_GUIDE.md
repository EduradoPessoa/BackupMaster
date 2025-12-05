# 🔒 Lidando com Arquivos Abertos/Bloqueados

## 🎯 O Problema

Durante backups, alguns arquivos podem estar:
- **Abertos** por aplicações
- **Bloqueados** pelo sistema operacional
- **Em uso** por outros processos
- **Protegidos** por permissões

Isso causa erros como:
```
PermissionError: [Errno 13] Permission denied
OSError: [Errno 5] Input/output error
```

---

## ✅ Soluções Implementadas

### **Módulo**: `backupmaster/locked_files.py`

Implementa **4 estratégias** para contornar o problema:

---

## 📋 Estratégias

### **1. Retry com Delay** ⏱️

**Como funciona**:
- Tenta copiar o arquivo
- Se falhar, aguarda 0.5s
- Tenta novamente (até 3 vezes)

**Quando usar**:
- Arquivos temporariamente bloqueados
- Processos que liberam arquivo rapidamente

**Código**:
```python
for attempt in range(max_retries):
    try:
        shutil.copy2(src, dst)
        return True
    except PermissionError:
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
            continue
```

---

### **2. Modo Compartilhado** 🤝

**Como funciona**:
- Abre arquivo em modo de leitura compartilhada
- Permite que outros processos também leiam
- Copia em chunks de 1MB

**Quando usar**:
- Arquivos de log
- Bancos de dados em uso
- Arquivos abertos para leitura

**Código**:
```python
with open(src, 'rb') as fsrc:
    with open(dst, 'wb') as fdst:
        while True:
            chunk = fsrc.read(1024 * 1024)  # 1MB
            if not chunk:
                break
            fdst.write(chunk)
```

**Vantagens**:
- ✅ Funciona com arquivos abertos para leitura
- ✅ Não sobrecarrega memória
- ✅ Multiplataforma

---

### **3. Volume Shadow Copy (VSS)** 💾

**Como funciona** (Windows):
- Cria snapshot do volume
- Copia do snapshot (não do arquivo original)
- Arquivo pode estar bloqueado no original

**Quando usar**:
- Bancos de dados (SQL Server, etc)
- Arquivos críticos do sistema
- Backups em produção

**Requisitos**:
```bash
pip install pywin32
```

**Código** (simplificado):
```python
import win32com.client

# Cria shadow copy
vss = win32com.client.Dispatch("VssBackupComponents")
# Copia do snapshot
```

**Vantagens**:
- ✅ Copia arquivos bloqueados
- ✅ Consistência de dados
- ✅ Usado por ferramentas profissionais

**Desvantagens**:
- ❌ Apenas Windows
- ❌ Requer privilégios de administrador
- ❌ Mais lento

---

### **4. Skip Automático** ⏭️

**Como funciona**:
- Identifica arquivos que sempre estão bloqueados
- Pula automaticamente
- Registra em log

**Arquivos pulados automaticamente**:
```python
skip_patterns = [
    'pagefile.sys',      # Arquivo de paginação
    'hiberfil.sys',      # Hibernação
    'swapfile.sys',      # Swap
    '$Recycle.Bin',      # Lixeira
    'System Volume Information',  # Sistema
    'NTUSER.DAT',        # Registro do usuário
    'UsrClass.dat',      # Classes do usuário
    '.lock',             # Arquivos de lock
    '.lck'               # Arquivos de lock
]
```

---

## 🚀 Como Usar

### **Uso Básico**:

```python
from backupmaster.locked_files import LockedFileHandler

# Cria handler
handler = LockedFileHandler(
    max_retries=3,      # Número de tentativas
    retry_delay=0.5     # Delay entre tentativas
)

# Copia arquivo
success, error = handler.copy_file_safe(
    src='C:\\arquivo.txt',
    dst='D:\\backup\\arquivo.txt',
    use_vss=False  # True para usar VSS
)

if success:
    print("Copiado!")
else:
    print(f"Erro: {error}")

# Ver resumo
summary = handler.get_summary()
print(f"Copiados: {summary['copied']}")
print(f"Pulados: {summary['skipped']}")
```

### **Copiar Diretório Inteiro**:

```python
from backupmaster.locked_files import copy_directory_safe

# Callback de progresso
def progress(current, total, filename):
    print(f"[{current}/{total}] {filename}")

# Copia diretório
summary = copy_directory_safe(
    src_dir='C:\\Users\\Documents',
    dst_dir='D:\\Backup\\Documents',
    skip_locked=True,      # Pula arquivos bloqueados
    use_vss=False,         # Usar VSS
    progress_callback=progress
)

print(f"Total: {summary['total_files']}")
print(f"Copiados: {summary['copied']}")
print(f"Pulados: {summary['skipped']}")
print(f"Erros: {summary['errors']}")
```

---

## 🔧 Integração com BackupEngine

### **Modificar `core.py`**:

```python
from backupmaster.locked_files import LockedFileHandler, should_skip_file

class BackupEngine:
    def create_backup(self, ...):
        handler = LockedFileHandler()
        
        for file in files_to_backup:
            # Pula arquivos do sistema
            if should_skip_file(file):
                continue
            
            # Copia com tratamento de bloqueio
            success, error = handler.copy_file_safe(
                src=file,
                dst=backup_path,
                use_vss=self.use_vss
            )
            
            if not success:
                logger.warning(f"Pulado: {file} - {error}")
        
        # Adiciona resumo ao resultado
        summary = handler.get_summary()
        result['skipped_files'] = summary['skipped']
        result['errors'] = summary['errors']
```

---

## 📊 Estatísticas

Após backup, você terá:

```python
{
    'total_files': 1000,
    'copied': 985,
    'skipped': 15,
    'errors': 15,
    'skipped_files': [
        'C:\\pagefile.sys',
        'C:\\Users\\user\\NTUSER.DAT',
        ...
    ],
    'error_details': [
        ('C:\\arquivo.db', 'PermissionError: [Errno 13]'),
        ...
    ]
}
```

---

## 🎯 Melhores Práticas

### **1. Sempre Use Skip**:
```python
skip_locked=True  # Não falhe o backup inteiro
```

### **2. Log de Arquivos Pulados**:
```python
if summary['skipped'] > 0:
    with open('skipped_files.log', 'w') as f:
        for file in summary['skipped_files']:
            f.write(f"{file}\n")
```

### **3. Notifique o Usuário**:
```python
if summary['skipped'] > 0:
    print(f"⚠️ {summary['skipped']} arquivos pulados")
    print("Ver: skipped_files.log")
```

### **4. Use VSS para Backups Críticos**:
```python
# Apenas para backups importantes
use_vss = (backup_type == 'production')
```

---

## 🔍 Identificar Quem Está Usando Arquivo

### **Windows**:

```python
from backupmaster.locked_files import get_file_lock_info

info = get_file_lock_info('C:\\arquivo.txt')

if info['locked']:
    print(f"Arquivo bloqueado por:")
    print(f"  Processo: {info['process']}")
    print(f"  PID: {info['pid']}")
```

**Requisito**:
```bash
pip install psutil
```

---

## ⚠️ Limitações

### **Modo Compartilhado**:
- ❌ Não funciona com arquivos abertos para escrita exclusiva
- ❌ Pode copiar dados inconsistentes

### **VSS**:
- ❌ Apenas Windows
- ❌ Requer admin
- ❌ Mais lento
- ❌ Requer pywin32

### **Retry**:
- ❌ Não funciona com bloqueios permanentes
- ❌ Adiciona delay ao backup

---

## 🚀 Roadmap

### **Futuras Melhorias**:

1. **Implementação Completa de VSS**:
   - Criar/gerenciar shadow copies
   - Copiar do snapshot
   - Limpar snapshots

2. **Linux LVM Snapshots**:
   - Equivalente ao VSS para Linux
   - Usar LVM para snapshots

3. **Notificações Inteligentes**:
   - Avisar usuário sobre arquivos bloqueados
   - Sugerir fechar aplicações

4. **Retry Inteligente**:
   - Detectar tipo de bloqueio
   - Ajustar estratégia automaticamente

5. **Backup Diferencial de Arquivos Bloqueados**:
   - Copiar apenas partes modificadas
   - Usar rsync-like algorithm

---

## 📝 Exemplo Completo

```python
from backupmaster.locked_files import copy_directory_safe

def backup_with_locked_files():
    print("Iniciando backup...")
    
    summary = copy_directory_safe(
        src_dir='C:\\Users\\Documents',
        dst_dir='D:\\Backup\\Documents',
        skip_locked=True,
        use_vss=False,
        progress_callback=lambda c, t, f: print(f"[{c}/{t}] {f}")
    )
    
    print("\n✅ Backup concluído!")
    print(f"📊 Estatísticas:")
    print(f"  Total: {summary['total_files']}")
    print(f"  ✅ Copiados: {summary['copied']}")
    print(f"  ⏭️ Pulados: {summary['skipped']}")
    print(f"  ❌ Erros: {summary['errors']}")
    
    if summary['skipped'] > 0:
        print(f"\n⚠️ Arquivos pulados:")
        for file in summary['skipped_files'][:10]:  # Mostra primeiros 10
            print(f"  - {file}")
        
        if len(summary['skipped_files']) > 10:
            print(f"  ... e mais {len(summary['skipped_files']) - 10}")

if __name__ == '__main__':
    backup_with_locked_files()
```

---

## ✅ Resumo

### **Problema**: Arquivos bloqueados impedem backup

### **Soluções**:
1. ⏱️ **Retry** - Tenta novamente
2. 🤝 **Modo Compartilhado** - Lê enquanto outros usam
3. 💾 **VSS** - Copia do snapshot (Windows)
4. ⏭️ **Skip** - Pula e continua

### **Resultado**:
- ✅ Backup não falha
- ✅ Máximo de arquivos copiados
- ✅ Log de arquivos pulados
- ✅ Usuário informado

---

**Arquivos bloqueados não são mais um problema! 🚀**
