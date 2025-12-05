# Guia de Publicação no GitHub

## 🚀 Passo a Passo para Publicar no GitHub

### 1. Criar Conta no GitHub (se não tiver)
1. Acesse https://github.com/
2. Clique em "Sign up"
3. Siga as instruções

### 2. Criar Novo Repositório

#### Via Interface Web:
1. Acesse https://github.com/new
2. Preencha:
   - **Repository name**: `backupmaster`
   - **Description**: `Sistema Profissional de Backup - Incremental, Multi-Plataforma e Gratuito`
   - **Public** ou **Private**: Escolha conforme preferência
   - **NÃO** marque "Initialize this repository with a README"
3. Clique em "Create repository"

### 3. Configurar Git Local

#### Windows:
```cmd
# Execute o script de inicialização
init_git.bat
```

#### Linux/Mac:
```bash
# Dê permissão de execução
chmod +x init_git.sh

# Execute o script
./init_git.sh
```

### 4. Conectar ao GitHub

Após criar o repositório no GitHub, execute:

```bash
# Adicione o remote (substitua SEU-USUARIO pelo seu username)
git remote add origin https://github.com/SEU-USUARIO/backupmaster.git

# Renomeie branch para main
git branch -M main

# Envie para o GitHub
git push -u origin main
```

### 5. Configurar Autenticação

#### Opção 1: HTTPS (Recomendado)
```bash
# Configure seu nome e email
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Use Personal Access Token
# Crie em: https://github.com/settings/tokens
# Quando solicitar senha, use o token
```

#### Opção 2: SSH
```bash
# Gere chave SSH
ssh-keygen -t ed25519 -C "seu@email.com"

# Adicione ao SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Adicione chave pública no GitHub
# https://github.com/settings/keys
cat ~/.ssh/id_ed25519.pub

# Use URL SSH
git remote set-url origin git@github.com:SEU-USUARIO/backupmaster.git
```

## 📝 Atualizações Futuras

### Fazer Commit de Mudanças:
```bash
# Adicionar arquivos modificados
git add .

# Criar commit
git commit -m "Descrição das mudanças"

# Enviar para GitHub
git push
```

### Criar Nova Versão (Tag):
```bash
# Criar tag
git tag -a v1.0.1 -m "Versão 1.0.1 - Correções e melhorias"

# Enviar tag
git push origin v1.0.1
```

## 🌟 Melhorar Visibilidade

### 1. README Atrativo
O README.md já está criado com:
- ✅ Badges de versão, licença e plataforma
- ✅ Descrição clara
- ✅ Instruções de instalação
- ✅ Exemplos de uso
- ✅ Lista de recursos

### 2. Topics no GitHub
Adicione topics ao repositório:
- `backup`
- `backup-tool`
- `python`
- `pyqt6`
- `compression`
- `incremental-backup`
- `windows`
- `linux`
- `macos`

### 3. Releases
Crie releases no GitHub:
1. Vá em "Releases" → "Create a new release"
2. Tag: `v1.0.0`
3. Title: `BackupMaster v1.0.0 - Lançamento Inicial`
4. Descrição: Liste recursos e mudanças
5. Anexe arquivos (opcional)

### 4. GitHub Pages (Opcional)
Crie documentação online:
```bash
# Crie branch gh-pages
git checkout --orphan gh-pages

# Adicione index.html
echo "<h1>BackupMaster</h1>" > index.html

# Commit e push
git add index.html
git commit -m "Initial GitHub Pages"
git push origin gh-pages
```

Acesse em: `https://SEU-USUARIO.github.io/backupmaster/`

## 📊 Rastreamento de Usuários

### Opção 1: GitHub Issues
Usuários podem criar issues para se registrar:
```markdown
**Template de Registro:**
- Nome:
- Email:
- Organização:
- Uso:
```

### Opção 2: GitHub Discussions
Ative Discussions no repositório:
1. Settings → Features → Discussions
2. Crie categoria "Registrations"
3. Usuários postam informações

### Opção 3: Google Forms
1. Crie formulário: https://forms.google.com/
2. Adicione link no README
3. Colete respostas em planilha

### Opção 4: Servidor Próprio
```python
# Em backupmaster/auth.py, configure:
VALIDATION_SERVER = "https://seu-servidor.com/api/register"

def _send_registration(self, user_data: Dict):
    try:
        response = requests.post(
            self.VALIDATION_SERVER,
            json=user_data,
            timeout=5
        )
        return response.status_code == 200
    except:
        return False
```

## 🔐 Licenças Remotas (Opcional)

### Criar Arquivo de Licenças
```bash
# Crie repositório separado: backupmaster-licenses
# Arquivo: licenses.json
{
  "licenses": [
    {
      "token": "abc123...",
      "name": "João Silva",
      "email": "joao@email.com",
      "registered_at": "2025-12-05T13:00:00",
      "status": "active"
    }
  ],
  "blacklist": []
}
```

### Validação Online
```python
# Em backupmaster/auth.py
VALIDATION_SERVER = "https://raw.githubusercontent.com/SEU-USUARIO/backupmaster-licenses/main/licenses.json"

def _validate_online(self) -> bool:
    try:
        response = requests.get(self.VALIDATION_SERVER, timeout=5)
        data = response.json()
        
        # Verifica se token está na blacklist
        if self.user_data["token"] in data.get("blacklist", []):
            return False
        
        return True
    except:
        return self._validate_offline()
```

## 📈 Analytics

### GitHub Insights
Veja estatísticas em:
- Insights → Traffic → Views
- Insights → Traffic → Clones
- Insights → Community → Contributors

### Badges no README
Adicione badges para mostrar:
```markdown
![GitHub stars](https://img.shields.io/github/stars/SEU-USUARIO/backupmaster)
![GitHub forks](https://img.shields.io/github/forks/SEU-USUARIO/backupmaster)
![GitHub issues](https://img.shields.io/github/issues/SEU-USUARIO/backupmaster)
![GitHub downloads](https://img.shields.io/github/downloads/SEU-USUARIO/backupmaster/total)
```

## 🎯 Checklist de Publicação

- [ ] Repositório criado no GitHub
- [ ] Git inicializado localmente
- [ ] Primeiro commit realizado
- [ ] Remote configurado
- [ ] Push para GitHub concluído
- [ ] README.md revisado
- [ ] LICENSE adicionada
- [ ] Topics configurados
- [ ] Release v1.0.0 criada
- [ ] Documentação completa
- [ ] Sistema de licenciamento testado

## 🚀 Comandos Rápidos

```bash
# Inicializar tudo de uma vez
git init
git add .
git commit -m "Initial commit: BackupMaster v1.0.0"
git remote add origin https://github.com/SEU-USUARIO/backupmaster.git
git branch -M main
git push -u origin main

# Criar tag de versão
git tag -a v1.0.0 -m "BackupMaster v1.0.0 - Lançamento Inicial"
git push origin v1.0.0
```

## 📞 Suporte

Após publicar, adicione no README:
```markdown
## 📞 Suporte

- **Issues**: https://github.com/SEU-USUARIO/backupmaster/issues
- **Discussions**: https://github.com/SEU-USUARIO/backupmaster/discussions
- **Email**: seu@email.com
```

## 🎉 Pronto!

Seu BackupMaster está agora no GitHub e pronto para ser usado por milhares de pessoas!

Compartilhe em:
- Reddit (r/Python, r/opensource)
- Twitter/X
- LinkedIn
- Dev.to
- Hacker News

Boa sorte! 🚀
