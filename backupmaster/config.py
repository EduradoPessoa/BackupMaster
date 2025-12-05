"""
Sistema de Configuração do BackupMaster
Gerencia preferências do usuário incluindo estratégias de arquivos bloqueados
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from enum import Enum


class LockedFileStrategy(Enum):
    """Estratégias para lidar com arquivos bloqueados"""
    SKIP = "skip"                    # Pula arquivos bloqueados
    RETRY = "retry"                  # Tenta novamente com delay
    SHARED_MODE = "shared_mode"      # Modo de leitura compartilhada
    VSS = "vss"                      # Volume Shadow Copy (Windows)
    AUTO = "auto"                    # Escolhe automaticamente


class BackupPreset(Enum):
    """Presets de configuração"""
    FAST = "fast"                    # Rápido - pula arquivos bloqueados
    BALANCED = "balanced"            # Balanceado - retry + shared mode
    COMPLETE = "complete"            # Completo - todas as estratégias


class ConfigManager:
    """Gerenciador de configurações do BackupMaster"""
    
    DEFAULT_CONFIG = {
        # Estratégia de arquivos bloqueados
        'locked_files': {
            'strategy': LockedFileStrategy.AUTO.value,
            'max_retries': 3,
            'retry_delay': 0.5,
            'use_shared_mode': True,
            'use_vss': False,
            'skip_system_files': True,
            'log_skipped_files': True
        },
        
        # Configurações de backup
        'backup': {
            'default_format': 'zip',
            'compression_level': 6,
            'incremental_by_default': False,
            'verify_after_backup': False
        },
        
        # Interface
        'ui': {
            'show_notifications': True,
            'minimize_to_tray': True,
            'start_minimized': False,
            'theme': 'dark'
        },
        
        # Telemetria
        'telemetry': {
            'enabled': True,
            'anonymous': True
        },
        
        # Avançado
        'advanced': {
            'buffer_size': 1048576,  # 1MB
            'max_threads': 4,
            'temp_dir': None
        }
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Inicializa gerenciador de configurações
        
        Args:
            config_file: Caminho para arquivo de configuração
        """
        if config_file is None:
            config_file = str(Path.home() / ".backupmaster_config.json")
        
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Carrega configuração do arquivo"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                
                # Merge com configuração padrão (para novos campos)
                config = self.DEFAULT_CONFIG.copy()
                self._deep_update(config, loaded_config)
                return config
            except Exception as e:
                print(f"Erro ao carregar configuração: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Primeira execução - salva configuração padrão
            config = self.DEFAULT_CONFIG.copy()
            self.save_config(config)
            return config
    
    def save_config(self, config: Optional[Dict[str, Any]] = None):
        """Salva configuração no arquivo"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém valor de configuração
        
        Args:
            key: Chave no formato 'section.key' (ex: 'locked_files.strategy')
            default: Valor padrão se não encontrado
        
        Returns:
            Valor da configuração
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any, save: bool = True):
        """
        Define valor de configuração
        
        Args:
            key: Chave no formato 'section.key'
            value: Novo valor
            save: Se deve salvar imediatamente
        """
        keys = key.split('.')
        config = self.config
        
        # Navega até o penúltimo nível
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Define valor
        config[keys[-1]] = value
        
        if save:
            self.save_config()
    
    def apply_preset(self, preset: BackupPreset, save: bool = True):
        """
        Aplica preset de configuração
        
        Args:
            preset: Preset a aplicar
            save: Se deve salvar
        """
        if preset == BackupPreset.FAST:
            # Rápido - pula arquivos bloqueados
            self.config['locked_files'].update({
                'strategy': LockedFileStrategy.SKIP.value,
                'max_retries': 1,
                'retry_delay': 0.1,
                'use_shared_mode': False,
                'use_vss': False
            })
        
        elif preset == BackupPreset.BALANCED:
            # Balanceado - retry + shared mode
            self.config['locked_files'].update({
                'strategy': LockedFileStrategy.AUTO.value,
                'max_retries': 3,
                'retry_delay': 0.5,
                'use_shared_mode': True,
                'use_vss': False
            })
        
        elif preset == BackupPreset.COMPLETE:
            # Completo - todas as estratégias
            self.config['locked_files'].update({
                'strategy': LockedFileStrategy.AUTO.value,
                'max_retries': 5,
                'retry_delay': 1.0,
                'use_shared_mode': True,
                'use_vss': True
            })
        
        if save:
            self.save_config()
    
    def get_locked_files_config(self) -> Dict[str, Any]:
        """Retorna configuração de arquivos bloqueados"""
        return self.config.get('locked_files', {})
    
    def reset_to_defaults(self, save: bool = True):
        """Restaura configuração padrão"""
        self.config = self.DEFAULT_CONFIG.copy()
        if save:
            self.save_config()
    
    def _deep_update(self, base: dict, update: dict):
        """Atualiza dicionário recursivamente"""
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_update(base[key], value)
            else:
                base[key] = value
    
    def export_config(self, filepath: str):
        """Exporta configuração para arquivo"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def import_config(self, filepath: str, save: bool = True):
        """Importa configuração de arquivo"""
        with open(filepath, 'r', encoding='utf-8') as f:
            imported = json.load(f)
        
        self._deep_update(self.config, imported)
        
        if save:
            self.save_config()


# Singleton global
_config_manager = None


def get_config_manager() -> ConfigManager:
    """Retorna instância global do ConfigManager"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


# Exemplo de uso
if __name__ == '__main__':
    # Obtém configuração
    config = get_config_manager()
    
    # Lê valores
    strategy = config.get('locked_files.strategy')
    print(f"Estratégia atual: {strategy}")
    
    # Define valores
    config.set('locked_files.max_retries', 5)
    
    # Aplica preset
    config.apply_preset(BackupPreset.COMPLETE)
    
    # Mostra configuração
    print("\nConfiguração de arquivos bloqueados:")
    for key, value in config.get_locked_files_config().items():
        print(f"  {key}: {value}")
