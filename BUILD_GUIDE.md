# Guia de Build - Criar Executáveis

## 🎯 Objetivo

Criar executáveis standalone do BackupMaster para:
- **Windows** (.exe)
- **Linux** (binário)
- **macOS** (.app)

## 📦 Pré-requisitos

### Todos os Sistemas:
```bash
# Instale as dependências de build
pip install -r requirements-build.txt
```

Isso instalará:
- PyInstaller (para criar executáveis)

## 🔨 Como Buildar

### Windows

```cmd
# Execute o script de build
build_windows.bat
```

**Resultado:**
- `dist/BackupMaster.exe` - Interface gráfica
- `dist/backupmaster.exe` - Interface CLI

### Linux

```bash
# Dê permissão de execução
chmod +x build_linux.sh

# Execute o script de build
./build_linux.sh
```

**Resultado:**
- `dist/BackupMaster` - Interface gráfica
- `dist/backupmaster` - Interface CLI

### macOS

```bash
# Dê permissão de execução
chmod +x build_macos.sh

# Execute o script de build
./build_macos.sh
```

**Resultado:**
- `dist/BackupMaster.app` - Aplicativo macOS (GUI)
- `dist/backupmaster` - Interface CLI

## 📋 Processo de Build

O PyInstaller:

1. **Analisa** o código Python
2. **Coleta** todas as dependências
3. **Empacota** tudo em um executável
4. **Comprime** com UPX (opcional)
5. **Cria** executável standalone

### Vantagens:
- ✅ Não precisa instalar Python
- ✅ Não precisa instalar dependências
- ✅ Funciona em qualquer máquina
- ✅ Fácil distribuição

## 🎨 Customização

### Adicionar Ícone

1. **Crie um ícone**:
   - Windows: `.ico` (256x256)
   - Linux: `.png` (256x256)
   - macOS: `.icns` (512x512)

2. **Edite os arquivos .spec**:
   ```python
   icon='path/to/icon.ico'  # Windows
   icon='path/to/icon.png'  # Linux
   icon='path/to/icon.icns' # macOS
   ```

3. **Rebuild**:
   ```bash
   pyinstaller --clean --noconfirm backupmaster_gui.spec
   ```

### Reduzir Tamanho

Edite os arquivos `.spec`:

```python
# Desabilite UPX se causar problemas
upx=False,

# Exclua módulos não usados
excludes=['tkinter', 'matplotlib', 'numpy'],
```

## 📊 Tamanhos Esperados

| Plataforma | GUI | CLI |
|------------|-----|-----|
| Windows    | ~80 MB | ~50 MB |
| Linux      | ~90 MB | ~55 MB |
| macOS      | ~95 MB | ~60 MB |

*Tamanhos podem variar dependendo das dependências*

## 🚀 Distribuição

### Windows

1. **Criar Instalador** (opcional):
   - Use Inno Setup
   - Use NSIS
   - Ou distribua o .exe diretamente

2. **Zip para distribuição**:
   ```cmd
   cd dist
   tar -a -c -f BackupMaster-Windows.zip BackupMaster.exe backupmaster.exe
   ```

### Linux

1. **Criar .deb ou .rpm** (opcional):
   - Use fpm (Effing Package Management)
   - Ou distribua o binário diretamente

2. **Tar.gz para distribuição**:
   ```bash
   cd dist
   tar -czf BackupMaster-Linux.tar.gz BackupMaster backupmaster
   ```

### macOS

1. **Criar .dmg** (opcional):
   - Use create-dmg
   - Ou distribua o .app diretamente

2. **Zip para distribuição**:
   ```bash
   cd dist
   zip -r BackupMaster-macOS.zip BackupMaster.app backupmaster
   ```

## 🔍 Testar Executáveis

### Windows
```cmd
# GUI
dist\BackupMaster.exe

# CLI
dist\backupmaster.exe --help
dist\backupmaster.exe backup -s "C:\test" -d "C:\backup" -f zip
```

### Linux
```bash
# GUI
./dist/BackupMaster

# CLI
./dist/backupmaster --help
./dist/backupmaster backup -s "/home/test" -d "/backup" -f zip
```

### macOS
```bash
# GUI
open dist/BackupMaster.app

# CLI
./dist/backupmaster --help
./dist/backupmaster backup -s "/Users/test" -d "/backup" -f zip
```

## 🐛 Troubleshooting

### Erro: "Module not found"
```bash
# Adicione ao hiddenimports no .spec
hiddenimports=[
    'backupmaster',
    'backupmaster.core',
    'backupmaster.auth',
    'backupmaster.telemetry',
    'seu_modulo_faltando',
],
```

### Erro: "Failed to execute script"
```bash
# Build com modo debug
pyinstaller --debug=all backupmaster_gui.spec

# Execute e veja os erros
dist/BackupMaster.exe
```

### Executável muito grande
```python
# No .spec, exclua módulos não usados
excludes=[
    'tkinter',
    'matplotlib',
    'numpy',
    'pandas',
],
```

### Antivírus bloqueia
- É normal, executáveis PyInstaller são sinalizados
- Assine digitalmente o executável (Windows)
- Ou adicione exceção no antivírus

## 📦 GitHub Releases

### Criar Release com Executáveis

1. **Build em cada plataforma**:
   ```bash
   # Windows
   build_windows.bat
   
   # Linux
   ./build_linux.sh
   
   # macOS
   ./build_macos.sh
   ```

2. **Criar arquivos de distribuição**:
   ```bash
   # Windows
   cd dist && tar -a -c -f BackupMaster-v1.0.0-Windows.zip BackupMaster.exe backupmaster.exe
   
   # Linux
   cd dist && tar -czf BackupMaster-v1.0.0-Linux.tar.gz BackupMaster backupmaster
   
   # macOS
   cd dist && zip -r BackupMaster-v1.0.0-macOS.zip BackupMaster.app backupmaster
   ```

3. **Upload no GitHub**:
   - Vá em Releases → Create new release
   - Tag: `v1.0.0`
   - Anexe os arquivos .zip/.tar.gz
   - Publique

## 🎯 Checklist de Build

- [ ] Instalar PyInstaller
- [ ] Testar código Python funciona
- [ ] Buildar executável
- [ ] Testar executável
- [ ] Verificar tamanho
- [ ] Criar arquivo de distribuição
- [ ] Testar em máquina limpa
- [ ] Upload no GitHub Releases

## 💡 Dicas

1. **Build em VM limpa** para garantir que funciona sem dependências
2. **Teste em múltiplas versões** do SO
3. **Assine digitalmente** (Windows/macOS) para evitar avisos
4. **Documente requisitos** mínimos do sistema
5. **Forneça checksums** (SHA256) dos executáveis

## 📞 Suporte

Problemas com build?
- Veja logs em `build/` folder
- Use `--debug=all` flag
- Consulte: https://pyinstaller.org/

---

**Boa sorte com a distribuição! 🚀**
