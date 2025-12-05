"""
Utilitário para lidar com arquivos abertos/bloqueados durante backup
Implementa várias estratégias para contornar problemas de acesso
"""

import os
import shutil
import time
import tempfile
from pathlib import Path
from typing import Optional, Tuple
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LockedFileHandler:
    """Gerencia cópia de arquivos que podem estar bloqueados"""
    
    def __init__(self, max_retries: int = 3, retry_delay: float = 0.5):
        """
        Inicializa handler
        
        Args:
            max_retries: Número máximo de tentativas
            retry_delay: Delay entre tentativas em segundos
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.skipped_files = []
        self.copied_files = []
        self.errors = []
    
    def copy_file_safe(self, src: str, dst: str, use_vss: bool = False) -> Tuple[bool, Optional[str]]:
        """
        Copia arquivo com tratamento de bloqueio
        
        Args:
            src: Arquivo de origem
            dst: Arquivo de destino
            use_vss: Usar Volume Shadow Copy (Windows)
        
        Returns:
            (sucesso, mensagem_erro)
        """
        # Estratégia 1: Tentar cópia normal com retry
        for attempt in range(self.max_retries):
            try:
                # Cria diretório de destino se não existir
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                
                # Tenta copiar
                shutil.copy2(src, dst)
                self.copied_files.append(src)
                return True, None
                
            except PermissionError as e:
                if attempt < self.max_retries - 1:
                    logger.debug(f"Tentativa {attempt + 1} falhou para {src}, aguardando...")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    # Última tentativa falhou
                    error_msg = f"PermissionError: {str(e)}"
                    
                    # Estratégia 2: Tentar com VSS (Windows)
                    if use_vss and os.name == 'nt':
                        vss_success, vss_error = self._copy_with_vss(src, dst)
                        if vss_success:
                            return True, None
                        error_msg += f" | VSS: {vss_error}"
                    
                    # Estratégia 3: Tentar abrir em modo compartilhado
                    shared_success, shared_error = self._copy_shared_mode(src, dst)
                    if shared_success:
                        return True, None
                    error_msg += f" | Shared: {shared_error}"
                    
                    # Todas as estratégias falharam
                    self.skipped_files.append(src)
                    self.errors.append((src, error_msg))
                    return False, error_msg
                    
            except Exception as e:
                error_msg = f"{type(e).__name__}: {str(e)}"
                self.skipped_files.append(src)
                self.errors.append((src, error_msg))
                return False, error_msg
        
        return False, "Max retries exceeded"
    
    def _copy_shared_mode(self, src: str, dst: str) -> Tuple[bool, Optional[str]]:
        """
        Tenta copiar arquivo abrindo em modo compartilhado
        
        Args:
            src: Arquivo de origem
            dst: Arquivo de destino
        
        Returns:
            (sucesso, mensagem_erro)
        """
        try:
            # Abre arquivo de origem em modo compartilhado (permite leitura por outros)
            with open(src, 'rb') as fsrc:
                # Cria arquivo de destino
                with open(dst, 'wb') as fdst:
                    # Copia em chunks para não sobrecarregar memória
                    chunk_size = 1024 * 1024  # 1MB
                    while True:
                        chunk = fsrc.read(chunk_size)
                        if not chunk:
                            break
                        fdst.write(chunk)
            
            # Copia metadados (timestamp, etc)
            try:
                shutil.copystat(src, dst)
            except:
                pass  # Não crítico se falhar
            
            self.copied_files.append(src)
            logger.info(f"Copiado em modo compartilhado: {src}")
            return True, None
            
        except Exception as e:
            return False, str(e)
    
    def _copy_with_vss(self, src: str, dst: str) -> Tuple[bool, Optional[str]]:
        """
        Tenta copiar usando Volume Shadow Copy (Windows)
        
        Args:
            src: Arquivo de origem
            dst: Arquivo de destino
        
        Returns:
            (sucesso, mensagem_erro)
        """
        if os.name != 'nt':
            return False, "VSS only available on Windows"
        
        try:
            import win32com.client
            
            # Cria shadow copy
            vss = win32com.client.Dispatch("VssBackupComponents")
            # ... implementação completa de VSS seria complexa
            # Por enquanto, retorna False
            return False, "VSS not fully implemented"
            
        except ImportError:
            return False, "pywin32 not installed"
        except Exception as e:
            return False, str(e)
    
    def get_summary(self) -> dict:
        """Retorna resumo da operação"""
        return {
            'total_files': len(self.copied_files) + len(self.skipped_files),
            'copied': len(self.copied_files),
            'skipped': len(self.skipped_files),
            'errors': len(self.errors),
            'skipped_files': self.skipped_files,
            'error_details': self.errors
        }


def copy_directory_safe(src_dir: str, dst_dir: str, 
                       skip_locked: bool = True,
                       use_vss: bool = False,
                       progress_callback=None) -> dict:
    """
    Copia diretório inteiro com tratamento de arquivos bloqueados
    
    Args:
        src_dir: Diretório de origem
        dst_dir: Diretório de destino
        skip_locked: Se True, pula arquivos bloqueados; se False, gera erro
        use_vss: Tentar usar Volume Shadow Copy
        progress_callback: Função callback(current, total, filename)
    
    Returns:
        Dicionário com estatísticas da cópia
    """
    handler = LockedFileHandler()
    
    # Lista todos os arquivos
    all_files = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, src_dir)
            dst_file = os.path.join(dst_dir, rel_path)
            all_files.append((src_file, dst_file))
    
    total_files = len(all_files)
    
    # Copia cada arquivo
    for idx, (src_file, dst_file) in enumerate(all_files, 1):
        if progress_callback:
            progress_callback(idx, total_files, src_file)
        
        success, error = handler.copy_file_safe(src_file, dst_file, use_vss)
        
        if not success and not skip_locked:
            raise Exception(f"Failed to copy {src_file}: {error}")
    
    return handler.get_summary()


# Funções auxiliares para integração com BackupEngine

def should_skip_file(filepath: str) -> bool:
    """
    Verifica se arquivo deve ser pulado automaticamente
    
    Args:
        filepath: Caminho do arquivo
    
    Returns:
        True se deve pular
    """
    # Lista de arquivos/pastas que geralmente estão bloqueados
    skip_patterns = [
        'pagefile.sys',
        'hiberfil.sys',
        'swapfile.sys',
        '$Recycle.Bin',
        'System Volume Information',
        'NTUSER.DAT',
        'UsrClass.dat',
        '.lock',
        '.lck'
    ]
    
    filename = os.path.basename(filepath).lower()
    
    for pattern in skip_patterns:
        if pattern.lower() in filename:
            return True
    
    return False


def get_file_lock_info(filepath: str) -> dict:
    """
    Obtém informações sobre quem está usando o arquivo (Windows)
    
    Args:
        filepath: Caminho do arquivo
    
    Returns:
        Dicionário com informações do lock
    """
    info = {
        'locked': False,
        'process': None,
        'pid': None
    }
    
    if os.name != 'nt':
        return info
    
    try:
        import psutil
        
        # Verifica se arquivo está aberto
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                for item in proc.open_files():
                    if item.path == filepath:
                        info['locked'] = True
                        info['process'] = proc.info['name']
                        info['pid'] = proc.info['pid']
                        return info
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
    except ImportError:
        pass
    
    return info


# Exemplo de uso
if __name__ == '__main__':
    # Teste de cópia com arquivos bloqueados
    handler = LockedFileHandler()
    
    # Simula cópia
    success, error = handler.copy_file_safe(
        'C:\\arquivo_bloqueado.txt',
        'C:\\backup\\arquivo_bloqueado.txt',
        use_vss=False
    )
    
    if success:
        print("Arquivo copiado com sucesso!")
    else:
        print(f"Erro ao copiar: {error}")
    
    # Mostra resumo
    summary = handler.get_summary()
    print(f"\nResumo:")
    print(f"Total: {summary['total_files']}")
    print(f"Copiados: {summary['copied']}")
    print(f"Pulados: {summary['skipped']}")
    print(f"Erros: {summary['errors']}")
