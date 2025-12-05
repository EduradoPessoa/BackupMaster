"""
Core backup functionality
"""

import os
import hashlib
import json
import shutil
import zipfile
import tarfile
import py7zr
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Callable, Optional


class BackupEngine:
    """Motor principal de backup com suporte a múltiplos formatos"""
    
    SUPPORTED_FORMATS = ['zip', '7z', 'tar.gz', 'tar.bz2']
    
    def __init__(self):
        self.metadata_file = ".backupmaster_metadata.json"
        self.progress_callback: Optional[Callable] = None
        
    def set_progress_callback(self, callback: Callable):
        """Define callback para atualização de progresso"""
        self.progress_callback = callback
        
    def _update_progress(self, current: int, total: int, message: str):
        """Atualiza o progresso se callback estiver definido"""
        if self.progress_callback:
            percentage = int((current / total) * 100) if total > 0 else 0
            self.progress_callback(percentage, message)
    
    def _calculate_file_hash(self, filepath: str) -> str:
        """Calcula hash MD5 de um arquivo"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"Erro ao calcular hash de {filepath}: {e}")
            return ""
    
    def _load_metadata(self, dest_dir: str) -> Dict:
        """Carrega metadados de backups anteriores"""
        metadata_path = os.path.join(dest_dir, self.metadata_file)
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao carregar metadados: {e}")
        return {"files": {}, "backups": []}
    
    def _save_metadata(self, dest_dir: str, metadata: Dict):
        """Salva metadados dos backups"""
        metadata_path = os.path.join(dest_dir, self.metadata_file)
        try:
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar metadados: {e}")
    
    def _get_files_to_backup(self, source_dir: str, incremental: bool, metadata: Dict) -> List[str]:
        """Retorna lista de arquivos que precisam ser copiados"""
        files_to_backup = []
        total_files = 0
        
        # Conta total de arquivos primeiro
        for root, _, files in os.walk(source_dir):
            total_files += len(files)
        
        current_file = 0
        for root, _, files in os.walk(source_dir):
            for file in files:
                current_file += 1
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, source_dir)
                
                self._update_progress(
                    current_file, 
                    total_files, 
                    f"Analisando: {relative_path[:50]}..."
                )
                
                if incremental:
                    # Verifica se arquivo foi modificado
                    file_hash = self._calculate_file_hash(filepath)
                    if relative_path not in metadata["files"] or \
                       metadata["files"][relative_path] != file_hash:
                        files_to_backup.append(filepath)
                        metadata["files"][relative_path] = file_hash
                else:
                    files_to_backup.append(filepath)
                    file_hash = self._calculate_file_hash(filepath)
                    metadata["files"][relative_path] = file_hash
        
        return files_to_backup
    
    def _compress_zip(self, files: List[str], source_dir: str, output_file: str):
        """Comprime arquivos em formato ZIP"""
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for i, filepath in enumerate(files):
                arcname = os.path.relpath(filepath, source_dir)
                zipf.write(filepath, arcname)
                self._update_progress(
                    i + 1, 
                    len(files), 
                    f"Comprimindo: {arcname[:50]}..."
                )
    
    def _compress_7z(self, files: List[str], source_dir: str, output_file: str):
        """Comprime arquivos em formato 7z"""
        with py7zr.SevenZipFile(output_file, 'w') as archive:
            for i, filepath in enumerate(files):
                arcname = os.path.relpath(filepath, source_dir)
                archive.write(filepath, arcname)
                self._update_progress(
                    i + 1, 
                    len(files), 
                    f"Comprimindo (7z): {arcname[:50]}..."
                )
    
    def _compress_tar(self, files: List[str], source_dir: str, output_file: str, mode: str):
        """Comprime arquivos em formato TAR (gz ou bz2)"""
        with tarfile.open(output_file, mode) as tar:
            for i, filepath in enumerate(files):
                arcname = os.path.relpath(filepath, source_dir)
                tar.add(filepath, arcname)
                self._update_progress(
                    i + 1, 
                    len(files), 
                    f"Comprimindo (TAR): {arcname[:50]}..."
                )
    
    def create_backup(self, source_dir: str, dest_dir: str, 
                     format: str = 'zip', incremental: bool = False,
                     backup_name: Optional[str] = None) -> Dict:
        """
        Cria um backup da pasta source_dir
        
        Args:
            source_dir: Diretório de origem
            dest_dir: Diretório de destino
            format: Formato de compressão (zip, 7z, tar.gz, tar.bz2)
            incremental: Se True, faz backup incremental
            backup_name: Nome customizado do backup
            
        Returns:
            Dict com informações do backup criado
        """
        if format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Formato {format} não suportado. Use: {', '.join(self.SUPPORTED_FORMATS)}")
        
        # Cria diretório de destino se não existir
        os.makedirs(dest_dir, exist_ok=True)
        
        # Carrega metadados
        metadata = self._load_metadata(dest_dir)
        
        # Obtém arquivos para backup
        self._update_progress(0, 100, "Iniciando análise de arquivos...")
        files_to_backup = self._get_files_to_backup(source_dir, incremental, metadata)
        
        if not files_to_backup:
            return {
                "status": "skipped",
                "message": "Nenhum arquivo modificado encontrado",
                "files_count": 0,
                "size": 0
            }
        
        # Gera nome do arquivo de backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        source_name = os.path.basename(os.path.normpath(source_dir))
        
        if backup_name:
            base_name = backup_name
        else:
            backup_type = "incremental" if incremental else "full"
            base_name = f"{source_name}_{backup_type}_{timestamp}"
        
        # Define extensão baseada no formato
        if format == 'tar.gz':
            extension = '.tar.gz'
        elif format == 'tar.bz2':
            extension = '.tar.bz2'
        else:
            extension = f'.{format}'
        
        output_file = os.path.join(dest_dir, base_name + extension)
        
        # Comprime arquivos
        self._update_progress(0, 100, "Iniciando compressão...")
        
        if format == 'zip':
            self._compress_zip(files_to_backup, source_dir, output_file)
        elif format == '7z':
            self._compress_7z(files_to_backup, source_dir, output_file)
        elif format == 'tar.gz':
            self._compress_tar(files_to_backup, source_dir, output_file, 'w:gz')
        elif format == 'tar.bz2':
            self._compress_tar(files_to_backup, source_dir, output_file, 'w:bz2')
        
        # Calcula tamanhos
        total_size = sum(os.path.getsize(f) for f in files_to_backup)
        compressed_size = os.path.getsize(output_file)
        compression_ratio = ((total_size - compressed_size) / total_size * 100) if total_size > 0 else 0
        
        # Atualiza metadados
        backup_info = {
            "filename": os.path.basename(output_file),
            "timestamp": timestamp,
            "format": format,
            "incremental": incremental,
            "files_count": len(files_to_backup),
            "original_size": total_size,
            "compressed_size": compressed_size,
            "compression_ratio": round(compression_ratio, 2),
            "source_dir": source_dir
        }
        
        metadata["backups"].append(backup_info)
        self._save_metadata(dest_dir, metadata)
        
        self._update_progress(100, 100, "Backup concluído!")
        
        return {
            "status": "success",
            "backup_file": output_file,
            **backup_info
        }
    
    def list_backups(self, dest_dir: str) -> List[Dict]:
        """Lista todos os backups disponíveis"""
        metadata = self._load_metadata(dest_dir)
        return metadata.get("backups", [])
    
    def restore_backup(self, backup_file: str, restore_dir: str) -> Dict:
        """
        Restaura um backup
        
        Args:
            backup_file: Caminho do arquivo de backup
            restore_dir: Diretório onde restaurar
            
        Returns:
            Dict com informações da restauração
        """
        if not os.path.exists(backup_file):
            raise FileNotFoundError(f"Arquivo de backup não encontrado: {backup_file}")
        
        os.makedirs(restore_dir, exist_ok=True)
        
        # Detecta formato pelo nome do arquivo
        if backup_file.endswith('.zip'):
            self._restore_zip(backup_file, restore_dir)
        elif backup_file.endswith('.7z'):
            self._restore_7z(backup_file, restore_dir)
        elif backup_file.endswith('.tar.gz'):
            self._restore_tar(backup_file, restore_dir, 'r:gz')
        elif backup_file.endswith('.tar.bz2'):
            self._restore_tar(backup_file, restore_dir, 'r:bz2')
        else:
            raise ValueError("Formato de backup não reconhecido")
        
        return {
            "status": "success",
            "message": f"Backup restaurado em {restore_dir}",
            "restore_dir": restore_dir
        }
    
    def _restore_zip(self, backup_file: str, restore_dir: str):
        """Restaura backup ZIP"""
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            members = zipf.namelist()
            for i, member in enumerate(members):
                zipf.extract(member, restore_dir)
                self._update_progress(
                    i + 1, 
                    len(members), 
                    f"Extraindo: {member[:50]}..."
                )
    
    def _restore_7z(self, backup_file: str, restore_dir: str):
        """Restaura backup 7z"""
        with py7zr.SevenZipFile(backup_file, 'r') as archive:
            archive.extractall(restore_dir)
            self._update_progress(100, 100, "Extração concluída!")
    
    def _restore_tar(self, backup_file: str, restore_dir: str, mode: str):
        """Restaura backup TAR"""
        with tarfile.open(backup_file, mode) as tar:
            members = tar.getmembers()
            for i, member in enumerate(members):
                tar.extract(member, restore_dir)
                self._update_progress(
                    i + 1, 
                    len(members), 
                    f"Extraindo: {member.name[:50]}..."
                )
