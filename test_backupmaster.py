"""
Testes básicos para o BackupMaster
"""

import os
import tempfile
import shutil
from pathlib import Path
from backupmaster.core import BackupEngine


def test_backup_creation():
    """Testa criação de backup"""
    print("🧪 Testando criação de backup...")
    
    # Cria diretórios temporários
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = os.path.join(temp_dir, "source")
        dest_dir = os.path.join(temp_dir, "dest")
        
        os.makedirs(source_dir)
        os.makedirs(dest_dir)
        
        # Cria arquivos de teste
        test_files = [
            "arquivo1.txt",
            "arquivo2.txt",
            "subdir/arquivo3.txt"
        ]
        
        for file in test_files:
            filepath = os.path.join(source_dir, file)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(f"Conteúdo de {file}")
        
        # Cria backup
        engine = BackupEngine()
        result = engine.create_backup(
            source_dir=source_dir,
            dest_dir=dest_dir,
            format='zip',
            incremental=False
        )
        
        assert result["status"] == "success"
        assert result["files_count"] == len(test_files)
        assert os.path.exists(result["backup_file"])
        
        print(f"✅ Backup criado: {result['filename']}")
        print(f"   Arquivos: {result['files_count']}")
        print(f"   Economia: {result['compression_ratio']:.1f}%")


def test_incremental_backup():
    """Testa backup incremental"""
    print("\n🧪 Testando backup incremental...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = os.path.join(temp_dir, "source")
        dest_dir = os.path.join(temp_dir, "dest")
        
        os.makedirs(source_dir)
        os.makedirs(dest_dir)
        
        # Cria arquivo inicial
        file1 = os.path.join(source_dir, "arquivo1.txt")
        with open(file1, 'w') as f:
            f.write("Conteúdo inicial")
        
        engine = BackupEngine()
        
        # Primeiro backup (completo)
        result1 = engine.create_backup(
            source_dir=source_dir,
            dest_dir=dest_dir,
            format='zip',
            incremental=True
        )
        
        print(f"✅ Primeiro backup: {result1['files_count']} arquivo(s)")
        
        # Segundo backup sem mudanças (deve pular)
        result2 = engine.create_backup(
            source_dir=source_dir,
            dest_dir=dest_dir,
            format='zip',
            incremental=True
        )
        
        assert result2["status"] == "skipped"
        print(f"✅ Segundo backup: pulado (nenhuma mudança)")
        
        # Adiciona novo arquivo
        file2 = os.path.join(source_dir, "arquivo2.txt")
        with open(file2, 'w') as f:
            f.write("Novo arquivo")
        
        # Terceiro backup (incremental)
        result3 = engine.create_backup(
            source_dir=source_dir,
            dest_dir=dest_dir,
            format='zip',
            incremental=True
        )
        
        assert result3["status"] == "success"
        assert result3["files_count"] == 1  # Apenas o novo arquivo
        print(f"✅ Terceiro backup: {result3['files_count']} arquivo(s) novo(s)")


def test_multiple_formats():
    """Testa diferentes formatos de compressão"""
    print("\n🧪 Testando múltiplos formatos...")
    
    formats = ['zip', '7z', 'tar.gz', 'tar.bz2']
    
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = os.path.join(temp_dir, "source")
        
        os.makedirs(source_dir)
        
        # Cria arquivo de teste
        test_file = os.path.join(source_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("Teste de compressão" * 100)
        
        engine = BackupEngine()
        
        for fmt in formats:
            dest_dir = os.path.join(temp_dir, f"dest_{fmt}")
            os.makedirs(dest_dir)
            
            result = engine.create_backup(
                source_dir=source_dir,
                dest_dir=dest_dir,
                format=fmt,
                incremental=False
            )
            
            assert result["status"] == "success"
            print(f"✅ Formato {fmt.upper()}: {result['compression_ratio']:.1f}% economia")


def test_restore():
    """Testa restauração de backup"""
    print("\n🧪 Testando restauração...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = os.path.join(temp_dir, "source")
        dest_dir = os.path.join(temp_dir, "dest")
        restore_dir = os.path.join(temp_dir, "restore")
        
        os.makedirs(source_dir)
        os.makedirs(dest_dir)
        
        # Cria arquivo de teste
        test_content = "Conteúdo de teste para restauração"
        test_file = os.path.join(source_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        # Cria backup
        engine = BackupEngine()
        result = engine.create_backup(
            source_dir=source_dir,
            dest_dir=dest_dir,
            format='zip',
            incremental=False
        )
        
        backup_file = result["backup_file"]
        print(f"✅ Backup criado: {os.path.basename(backup_file)}")
        
        # Restaura backup
        restore_result = engine.restore_backup(backup_file, restore_dir)
        
        assert restore_result["status"] == "success"
        
        # Verifica se arquivo foi restaurado
        restored_file = os.path.join(restore_dir, "test.txt")
        assert os.path.exists(restored_file)
        
        with open(restored_file, 'r') as f:
            restored_content = f.read()
        
        assert restored_content == test_content
        print(f"✅ Arquivo restaurado corretamente")


def test_list_backups():
    """Testa listagem de backups"""
    print("\n🧪 Testando listagem de backups...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = os.path.join(temp_dir, "source")
        dest_dir = os.path.join(temp_dir, "dest")
        
        os.makedirs(source_dir)
        os.makedirs(dest_dir)
        
        # Cria arquivo de teste
        test_file = os.path.join(source_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("Teste")
        
        engine = BackupEngine()
        
        # Cria múltiplos backups
        for i in range(3):
            engine.create_backup(
                source_dir=source_dir,
                dest_dir=dest_dir,
                format='zip',
                incremental=False,
                backup_name=f"backup_{i}"
            )
        
        # Lista backups
        backups = engine.list_backups(dest_dir)
        
        assert len(backups) == 3
        print(f"✅ {len(backups)} backup(s) listado(s)")
        
        for backup in backups:
            print(f"   - {backup['filename']}")


def run_all_tests():
    """Executa todos os testes"""
    print("=" * 60)
    print("🔄 BackupMaster - Suite de Testes")
    print("=" * 60)
    
    try:
        test_backup_creation()
        test_incremental_backup()
        test_multiple_formats()
        test_restore()
        test_list_backups()
        
        print("\n" + "=" * 60)
        print("✅ Todos os testes passaram com sucesso!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ Teste falhou: {e}")
    except Exception as e:
        print(f"\n❌ Erro durante teste: {e}")


if __name__ == '__main__':
    run_all_tests()
