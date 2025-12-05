# 🚀 Guia Rápido de Deploy - 5 Minutos

## Passo 1: MySQL (2 min)
```
cPanel → MySQL Databases
├── Criar banco: backupmaster_telemetry
├── Criar usuário: backupmaster_user
└── Adicionar usuário ao banco (ALL PRIVILEGES)

phpMyAdmin → Import → database.sql
```

## Passo 2: Configurar (1 min)
```php
// Edite api/config.php
define('DB_NAME', 'u123_backupmaster'); // Nome COMPLETO
define('DB_USER', 'u123_user');          // Nome COMPLETO  
define('DB_PASS', 'sua_senha');
define('ADMIN_PASSWORD', 'senha_admin');
```

```javascript
// Edite dashboard.js linha 8
const API_URL = 'https://seu-dominio.com/api/telemetry.php';
```

## Passo 3: Upload (1 min)
```
FileZilla → public_html/
├── index.html
├── dashboard.js
└── api/
    ├── config.php (permissão 600)
    └── telemetry.php
```

## Passo 4: Testar (1 min)
```
✅ https://seu-dominio.com/api/telemetry.php?type=public
✅ https://seu-dominio.com/
```

## ✅ Pronto!
Dashboard funcionando em 5 minutos! 🎉
