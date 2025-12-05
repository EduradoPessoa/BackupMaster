# Dashboard de Telemetria - BackupMaster

## 🎯 Visão Geral

Dashboard web moderno para visualizar estatísticas de uso do BackupMaster.

### Características:
- ✅ **Design Moderno** - Interface estilo ShadCN com TailwindCSS
- ✅ **Estatísticas em Tempo Real** - Atualização automática
- ✅ **Painel Admin** - Visualização de usuários e tokens
- ✅ **Responsivo** - Funciona em desktop e mobile
- ✅ **Sem Dependências** - HTML/CSS/JS puro

## 📊 Estatísticas Públicas

### Visíveis para Todos:
- Total de usuários
- Usuários ativos (30 dias)
- Total de backups realizados
- Terabytes backupeados
- Downloads por plataforma
- Formatos mais usados

## 🔐 Painel Administrativo

### Acesso Restrito (Requer Senha):
- Lista completa de usuários
- Emails e tokens
- Estatísticas individuais
- Busca e filtros
- Último acesso

### Senha Padrão:
```
backupmaster2025
```

**⚠️ IMPORTANTE**: Altere a senha em `dashboard.js` linha 3:
```javascript
const ADMIN_PASSWORD = 'sua_senha_segura_aqui';
```

## 🚀 Como Usar

### Opção 1: Servidor Python (Recomendado)

```bash
# Execute o servidor
python serve_dashboard.py

# Acesse no navegador
http://localhost:8000
```

### Opção 2: Abrir Diretamente

```bash
# Abra o arquivo no navegador
web/index.html
```

## 📁 Estrutura

```
web/
├── index.html      # Interface do dashboard
└── dashboard.js    # Lógica e dados
```

## 🎨 Customização

### Alterar Cores

Edite `index.html` e modifique as classes Tailwind:

```html
<!-- Gradiente do header -->
<header class="gradient-bg">
  <!-- Altere em style: -->
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
</header>
```

### Adicionar Dados Reais

Edite `dashboard.js` e substitua `telemetryData`:

```javascript
// Carregue de uma API
fetch('/api/telemetry')
  .then(res => res.json())
  .then(data => {
    telemetryData = data;
    loadDashboardData();
  });
```

## 🔌 Integração com API

### Criar API Backend

```python
# api.py
from flask import Flask, jsonify
from backupmaster.telemetry import GlobalStatsCollector

app = Flask(__name__)

@app.route('/api/telemetry')
def get_telemetry():
    collector = GlobalStatsCollector()
    stats = collector.get_global_stats()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(port=5000)
```

### Conectar Frontend

```javascript
// dashboard.js
async function loadDashboardData() {
    const response = await fetch('http://localhost:5000/api/telemetry');
    const data = await response.json();
    
    telemetryData = data;
    updateUI();
}
```

## 📊 Dados de Exemplo

O dashboard vem com dados simulados para demonstração:

- **1.250 usuários** registrados
- **890 usuários ativos** (30 dias)
- **187.500 backups** realizados
- **6.250 TB** de dados protegidos

### Usuários de Exemplo:
1. João Silva - 150 backups, 5.2 TB
2. Maria Santos - 89 backups, 3.8 TB
3. Pedro Costa - 234 backups, 12.5 TB
4. Ana Oliveira - 67 backups, 2.1 TB
5. Carlos Mendes - 412 backups, 18.9 TB

## 🌐 Deploy

### GitHub Pages

1. **Crie branch gh-pages**:
   ```bash
   git checkout --orphan gh-pages
   git rm -rf .
   cp -r web/* .
   git add .
   git commit -m "Deploy dashboard"
   git push origin gh-pages
   ```

2. **Acesse**:
   ```
   https://seu-usuario.github.io/backupmaster/
   ```

### Netlify

1. **Conecte repositório**
2. **Configure build**:
   - Build command: (vazio)
   - Publish directory: `web`
3. **Deploy**

### Vercel

```bash
# Instale Vercel CLI
npm i -g vercel

# Deploy
cd web
vercel
```

## 🔒 Segurança

### Recomendações:

1. **Altere a senha padrão**
2. **Use HTTPS** em produção
3. **Implemente autenticação real** (JWT, OAuth)
4. **Valide no backend** - nunca confie apenas no frontend
5. **Rate limiting** para prevenir ataques

### Autenticação Real (Exemplo):

```javascript
// Substitua por autenticação JWT
async function handleLogin(e) {
    e.preventDefault();
    
    const response = await fetch('/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            password: document.getElementById('adminPassword').value
        })
    });
    
    const data = await response.json();
    
    if (data.token) {
        localStorage.setItem('adminToken', data.token);
        showAdminSection();
    }
}
```

## 📱 Responsividade

O dashboard é totalmente responsivo:

- **Desktop**: Grade de 4 colunas
- **Tablet**: Grade de 2 colunas
- **Mobile**: 1 coluna

## 🎯 Recursos

### Animações:
- ✅ Números animados ao carregar
- ✅ Barras de progresso animadas
- ✅ Hover effects nos cards
- ✅ Transições suaves

### Interatividade:
- ✅ Busca em tempo real
- ✅ Copiar token com um clique
- ✅ Modal de login
- ✅ Atualização automática

## 📞 Suporte

Problemas com o dashboard?
- Verifique o console do navegador (F12)
- Teste em modo incógnito
- Limpe o cache do navegador

## 🔄 Atualizações Futuras

Planejado:
- [ ] Gráficos interativos (Chart.js)
- [ ] Exportar dados (CSV, JSON)
- [ ] Filtros avançados
- [ ] Notificações em tempo real
- [ ] Dark mode
- [ ] Multi-idioma

---

**Dashboard criado com ❤️ para BackupMaster**
