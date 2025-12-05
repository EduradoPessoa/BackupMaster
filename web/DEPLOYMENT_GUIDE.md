# 🚀 Guia de Implantação - BackupMaster Dashboard na Hostinger

## 📋 Índice
1. [Pré-requisitos](#pré-requisitos)
2. [Configurar Banco de Dados MySQL](#configurar-banco-de-dados-mysql)
3. [Preparar Arquivos Localmente](#preparar-arquivos-localmente)
4. [Upload via FTP](#upload-via-ftp)
5. [Configurar API PHP](#configurar-api-php)
6. [Testar Dashboard](#testar-dashboard)
7. [Configurar Domínio](#configurar-domínio)
8. [Segurança](#segurança)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Pré-requisitos

### O que você precisa:
- ✅ Conta na Hostinger (qualquer plano com PHP e MySQL)
- ✅ Domínio configurado (ex: `backupmaster.com.br`)
- ✅ Cliente FTP (FileZilla recomendado)
- ✅ Acesso ao cPanel da Hostinger

### Verificar recursos do servidor:
- PHP 7.4 ou superior
- MySQL 5.7 ou superior
- Extensões PHP: PDO, PDO_MySQL, JSON

---

## 📊 Passo 1: Configurar Banco de Dados MySQL

### 1.1 Acessar cPanel

1. **Login na Hostinger**: https://hpanel.hostinger.com/
2. **Selecione** seu plano de hospedagem
3. **Clique** em "Gerenciar" → "Painel de Controle" (cPanel)

### 1.2 Criar Banco de Dados

1. **No cPanel**, procure por "**MySQL Databases**" ou "**Bancos de Dados MySQL**"
2. **Criar novo banco de dados**:
   ```
   Nome: backupmaster_telemetry
   ```
   - Se o sistema adicionar prefixo, ficará algo como: `u123456789_backupmaster`
   - **Anote o nome completo!**

3. **Criar usuário MySQL**:
   ```
   Usuário: backupmaster_user
   Senha: [Gere uma senha forte]
   ```
   - **Anote usuário e senha!**

4. **Adicionar usuário ao banco**:
   - Selecione o usuário criado
   - Selecione o banco criado
   - Marque "**ALL PRIVILEGES**" (Todos os privilégios)
   - Clique em "**Add**" ou "**Adicionar**"

### 1.3 Importar Estrutura do Banco

1. **No cPanel**, procure por "**phpMyAdmin**"
2. **Selecione** o banco `backupmaster_telemetry` (ou nome com prefixo)
3. **Clique** na aba "**Import**" ou "**Importar**"
4. **Escolha** o arquivo `database.sql` do seu computador
5. **Clique** em "**Go**" ou "**Executar**"

✅ **Sucesso**: Você verá as tabelas criadas: `users`, `user_stats`, `downloads`, `events`

---

## 📦 Passo 2: Preparar Arquivos Localmente

### 2.1 Estrutura de Pastas

Crie esta estrutura no seu computador:

```
backupmaster-web/
├── index.html
├── dashboard.js
└── api/
    ├── config.php
    └── telemetry.php
```

### 2.2 Copiar Arquivos

**Do projeto BackupMaster**:
```bash
# Copie estes arquivos:
web/index.html          → backupmaster-web/index.html
web/dashboard.js        → backupmaster-web/dashboard.js
web/api/telemetry.php   → backupmaster-web/api/telemetry.php
```

### 2.3 Criar config.php

**Copie** `web/api/config.example.php` para `backupmaster-web/api/config.php`

**Edite** `config.php` com as credenciais do MySQL:

```php
<?php
// Configurações do MySQL (Hostinger)
define('DB_HOST', 'localhost');
define('DB_NAME', 'u123456789_backupmaster'); // Nome COMPLETO do banco
define('DB_USER', 'u123456789_user');          // Nome COMPLETO do usuário
define('DB_PASS', 'SUA_SENHA_AQUI');           // Senha que você criou
define('DB_CHARSET', 'utf8mb4');

// Senha do Admin (ALTERE!)
define('ADMIN_PASSWORD', 'SuaSenhaSeguraAqui123!');

// Configurações de CORS
define('ALLOWED_ORIGINS', [
    'https://seu-dominio.com',
    'https://www.seu-dominio.com'
]);

// Timezone
date_default_timezone_set('America/Sao_Paulo');

// Configurações de erro (DESABILITE em produção)
ini_set('display_errors', 0);
error_reporting(0);

// ... resto do arquivo igual
```

### 2.4 Atualizar dashboard.js

**Edite** `dashboard.js` linha 8:

```javascript
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/api/telemetry.php'
    : 'https://seu-dominio.com/api/telemetry.php'; // ALTERE AQUI!
```

---

## 📤 Passo 3: Upload via FTP

### 3.1 Obter Credenciais FTP

**No cPanel da Hostinger**:
1. Procure por "**FTP Accounts**" ou "**Contas FTP**"
2. **Anote**:
   - Host: `ftp.seu-dominio.com` ou IP fornecido
   - Usuário: geralmente o mesmo do cPanel
   - Senha: a mesma do cPanel
   - Porta: `21` (FTP) ou `22` (SFTP)

### 3.2 Conectar com FileZilla

1. **Baixe FileZilla**: https://filezilla-project.org/
2. **Abra FileZilla**
3. **Preencha**:
   ```
   Host: ftp.seu-dominio.com
   Usuário: seu_usuario_ftp
   Senha: sua_senha_ftp
   Porta: 21
   ```
4. **Clique** em "Quickconnect" ou "Conexão Rápida"

### 3.3 Navegar para public_html

**No lado direito** (servidor remoto):
1. **Navegue** até `/public_html/` ou `/domains/seu-dominio.com/public_html/`
2. Esta é a pasta raiz do seu site

### 3.4 Upload dos Arquivos

**Arraste** os arquivos do lado esquerdo (seu computador) para o lado direito (servidor):

```
public_html/
├── index.html          ← Arraste aqui
├── dashboard.js        ← Arraste aqui
└── api/                ← Crie pasta e arraste arquivos
    ├── config.php
    └── telemetry.php
```

**Passos**:
1. **Arraste** `index.html` para `public_html/`
2. **Arraste** `dashboard.js` para `public_html/`
3. **Crie pasta** `api` dentro de `public_html/`
4. **Arraste** `config.php` e `telemetry.php` para `public_html/api/`

✅ **Estrutura final no servidor**:
```
/public_html/
├── index.html
├── dashboard.js
└── api/
    ├── config.php
    └── telemetry.php
```

---

## ⚙️ Passo 4: Configurar Permissões

### 4.1 Permissões de Arquivos

**No FileZilla**, clique com botão direito em cada arquivo:

```
index.html      → 644 (rw-r--r--)
dashboard.js    → 644 (rw-r--r--)
api/config.php  → 600 (rw-------)  ← IMPORTANTE!
api/telemetry.php → 644 (rw-r--r--)
```

**Como alterar**:
1. Botão direito no arquivo → "**File permissions**"
2. Digite o número (ex: `644`)
3. OK

### 4.2 Permissões de Pastas

```
api/            → 755 (rwxr-xr-x)
```

---

## 🧪 Passo 5: Testar Dashboard

### 5.1 Testar API

**Abra no navegador**:
```
https://seu-dominio.com/api/telemetry.php?type=public
```

**Deve retornar JSON**:
```json
{
  "success": true,
  "data": {
    "total_users": 3,
    "active_users_30d": 3,
    "total_backups": 473,
    ...
  }
}
```

❌ **Se der erro**:
- Verifique `config.php` (credenciais do MySQL)
- Verifique se o banco foi importado
- Veja logs de erro no cPanel

### 5.2 Testar Dashboard

**Abra no navegador**:
```
https://seu-dominio.com/
```

**Deve mostrar**:
- ✅ Estatísticas animadas
- ✅ Gráficos de downloads
- ✅ Gráficos de formatos
- ✅ Botão "Admin"

### 5.3 Testar Painel Admin

1. **Clique** em "Admin"
2. **Digite** a senha que você configurou em `config.php`
3. **Deve mostrar** tabela de usuários

---

## 🌐 Passo 6: Configurar Domínio (Opcional)

### 6.1 Subdomínio

Se quiser usar `stats.seu-dominio.com`:

**No cPanel**:
1. **Subdomains** ou "**Subdomínios**"
2. **Criar**:
   ```
   Subdomínio: stats
   Document Root: /public_html/stats
   ```
3. **Upload** arquivos para `/public_html/stats/`

### 6.2 SSL/HTTPS

**No cPanel da Hostinger**:
1. Procure "**SSL/TLS**" ou "**Let's Encrypt**"
2. **Ative SSL** para seu domínio
3. **Force HTTPS** (recomendado)

**Adicione** ao `.htaccess` em `public_html/`:
```apache
# Force HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

---

## 🔒 Passo 7: Segurança

### 7.1 Proteger config.php

**Crie** arquivo `.htaccess` em `public_html/api/`:

```apache
# Bloquear acesso direto ao config.php
<Files "config.php">
    Order Allow,Deny
    Deny from all
</Files>

# Permitir apenas PHP
<FilesMatch "\.(php)$">
    Allow from all
</FilesMatch>
```

### 7.2 Alterar Senhas Padrão

**IMPORTANTE**: Altere estas senhas:

1. **Admin Dashboard** (`config.php` linha 13):
   ```php
   define('ADMIN_PASSWORD', 'SuaSenhaForte123!@#');
   ```

2. **MySQL** (se ainda não alterou)

### 7.3 Backup do Banco

**No cPanel**:
1. **phpMyAdmin** → Selecione banco
2. **Export** → **Go**
3. **Salve** o arquivo `.sql` localmente

**Configure backup automático**:
- Hostinger geralmente faz backup diário
- Verifique em "Backups" no cPanel

---

## 🐛 Passo 8: Troubleshooting

### Erro: "Database connection failed"

**Causa**: Credenciais incorretas em `config.php`

**Solução**:
1. Verifique nome do banco (com prefixo)
2. Verifique usuário (com prefixo)
3. Verifique senha
4. Teste conexão no phpMyAdmin

### Erro: "404 Not Found" na API

**Causa**: Arquivo não foi enviado ou caminho errado

**Solução**:
1. Verifique se `api/telemetry.php` existe
2. Verifique permissões (644)
3. Verifique URL no `dashboard.js`

### Erro: "CORS policy"

**Causa**: Domínio não está em `ALLOWED_ORIGINS`

**Solução**:
Edite `config.php`:
```php
define('ALLOWED_ORIGINS', [
    'https://seu-dominio.com',
    'https://www.seu-dominio.com',
    'http://localhost:8000' // Para testes locais
]);
```

### Dashboard não carrega dados

**Causa**: JavaScript não consegue conectar à API

**Solução**:
1. Abra Console do navegador (F12)
2. Veja erros
3. Verifique URL da API em `dashboard.js`
4. Teste API diretamente no navegador

### Senha admin não funciona

**Causa**: Senha em `config.php` diferente da digitada

**Solução**:
1. Verifique `config.php` linha 13
2. Senha é case-sensitive
3. Limpe cache do navegador

---

## 📊 Passo 9: Monitoramento

### 9.1 Ver Logs de Erro

**No cPanel**:
1. **Error Log** ou "**Logs de Erro**"
2. Veja erros PHP recentes

### 9.2 Estatísticas de Acesso

**No cPanel**:
1. **Awstats** ou "**Estatísticas**"
2. Veja visitantes do dashboard

### 9.3 Banco de Dados

**No phpMyAdmin**:
```sql
-- Ver total de usuários
SELECT COUNT(*) FROM users;

-- Ver usuários ativos
SELECT COUNT(*) FROM users 
WHERE last_validation >= DATE_SUB(NOW(), INTERVAL 30 DAY);

-- Ver total de backups
SELECT SUM(total_backups) FROM user_stats;
```

---

## ✅ Checklist Final

Antes de considerar concluído:

- [ ] Banco de dados criado e importado
- [ ] Credenciais MySQL corretas em `config.php`
- [ ] Arquivos enviados via FTP
- [ ] Permissões configuradas (config.php = 600)
- [ ] API testada e funcionando
- [ ] Dashboard carrega dados
- [ ] Painel admin funciona
- [ ] Senha admin alterada
- [ ] SSL/HTTPS ativado
- [ ] `.htaccess` protegendo config.php
- [ ] Backup do banco configurado

---

## 🎯 Resumo Rápido

```bash
1. cPanel → MySQL Databases → Criar banco
2. phpMyAdmin → Import database.sql
3. Editar config.php com credenciais
4. FileZilla → Upload arquivos para public_html/
5. Testar: https://seu-dominio.com/api/telemetry.php?type=public
6. Testar: https://seu-dominio.com/
7. Alterar senhas padrão
8. Ativar SSL
```

---

## 📞 Suporte Hostinger

Se tiver problemas:
- **Chat**: https://www.hostinger.com.br/
- **Email**: suporte@hostinger.com.br
- **Base de Conhecimento**: https://support.hostinger.com/

---

## 🚀 Próximos Passos

Após implantação:

1. **Integrar** BackupMaster Python para enviar dados
2. **Monitorar** estatísticas diariamente
3. **Fazer backup** do banco semanalmente
4. **Atualizar** conforme necessário

---

**Dashboard implantado com sucesso! 🎉**

Acesse: `https://seu-dominio.com`
