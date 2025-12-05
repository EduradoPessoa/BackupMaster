"""
Sistema de Telemetria e Estatísticas do BackupMaster
"""

import os
import json
import hashlib
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class TelemetryManager:
    """Gerenciador de telemetria e estatísticas"""
    
    # URL do servidor de telemetria (GitHub, Firebase, ou servidor próprio)
    TELEMETRY_SERVER = "https://api.github.com/repos/seu-usuario/backupmaster-stats/issues"
    
    # Arquivo local de estatísticas
    STATS_FILE = ".backupmaster_stats.json"
    
    def __init__(self):
        self.stats_path = self._get_stats_path()
        self.stats = self._load_stats()
        
    def _get_stats_path(self) -> str:
        """Retorna caminho do arquivo de estatísticas"""
        home = Path.home()
        return os.path.join(home, self.STATS_FILE)
    
    def _load_stats(self) -> Dict:
        """Carrega estatísticas locais"""
        if os.path.exists(self.stats_path):
            try:
                with open(self.stats_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao carregar estatísticas: {e}")
        
        # Estatísticas padrão
        return {
            "total_backups": 0,
            "total_bytes_original": 0,
            "total_bytes_compressed": 0,
            "total_files": 0,
            "backups_by_format": {
                "zip": 0,
                "7z": 0,
                "tar.gz": 0,
                "tar.bz2": 0
            },
            "incremental_backups": 0,
            "full_backups": 0,
            "first_backup": None,
            "last_backup": None,
            "total_space_saved": 0,
            "version": "1.0.0"
        }
    
    def _save_stats(self):
        """Salva estatísticas localmente"""
        try:
            with open(self.stats_path, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar estatísticas: {e}")
    
    def record_backup(self, backup_info: Dict):
        """
        Registra estatísticas de um backup
        
        Args:
            backup_info: Informações do backup (do BackupEngine)
        """
        # Atualiza contadores
        self.stats["total_backups"] += 1
        self.stats["total_bytes_original"] += backup_info.get("original_size", 0)
        self.stats["total_bytes_compressed"] += backup_info.get("compressed_size", 0)
        self.stats["total_files"] += backup_info.get("files_count", 0)
        
        # Economia de espaço
        original = backup_info.get("original_size", 0)
        compressed = backup_info.get("compressed_size", 0)
        self.stats["total_space_saved"] += (original - compressed)
        
        # Formato
        format_type = backup_info.get("format", "zip")
        if format_type in self.stats["backups_by_format"]:
            self.stats["backups_by_format"][format_type] += 1
        
        # Tipo de backup
        if backup_info.get("incremental", False):
            self.stats["incremental_backups"] += 1
        else:
            self.stats["full_backups"] += 1
        
        # Timestamps
        now = datetime.now().isoformat()
        if not self.stats["first_backup"]:
            self.stats["first_backup"] = now
        self.stats["last_backup"] = now
        
        # Salva
        self._save_stats()
        
        # Envia telemetria (opcional)
        self._send_telemetry()
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas locais"""
        return self.stats.copy()
    
    def get_formatted_stats(self) -> Dict:
        """Retorna estatísticas formatadas para exibição"""
        stats = self.stats.copy()
        
        # Formata tamanhos
        stats["total_tb_original"] = stats["total_bytes_original"] / (1024**4)
        stats["total_tb_compressed"] = stats["total_bytes_compressed"] / (1024**4)
        stats["total_tb_saved"] = stats["total_space_saved"] / (1024**4)
        
        stats["total_gb_original"] = stats["total_bytes_original"] / (1024**3)
        stats["total_gb_compressed"] = stats["total_bytes_compressed"] / (1024**3)
        stats["total_gb_saved"] = stats["total_space_saved"] / (1024**3)
        
        # Calcula porcentagem de economia
        if stats["total_bytes_original"] > 0:
            stats["compression_ratio"] = (
                stats["total_space_saved"] / stats["total_bytes_original"] * 100
            )
        else:
            stats["compression_ratio"] = 0
        
        # Calcula dias de uso
        if stats["first_backup"]:
            first = datetime.fromisoformat(stats["first_backup"])
            days = (datetime.now() - first).days
            stats["days_active"] = days
        else:
            stats["days_active"] = 0
        
        return stats
    
    def _send_telemetry(self):
        """
        Envia telemetria anonimizada para servidor
        (Implementação opcional e não-bloqueante)
        """
        try:
            # Apenas envia a cada 10 backups para não sobrecarregar
            if self.stats["total_backups"] % 10 != 0:
                return
            
            # Dados anonimizados
            telemetry_data = {
                "total_backups": self.stats["total_backups"],
                "total_tb": round(self.stats["total_bytes_original"] / (1024**4), 2),
                "formats": self.stats["backups_by_format"],
                "version": self.stats["version"],
                "timestamp": datetime.now().isoformat()
            }
            
            # Envia para servidor (implementar conforme necessário)
            # Exemplo: GitHub Issues, Firebase, webhook, etc.
            
            # Por enquanto, apenas log local
            log_file = os.path.join(Path.home(), ".backupmaster_telemetry.log")
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{json.dumps(telemetry_data)}\n")
                
        except Exception as e:
            # Falha silenciosa - não bloqueia o uso
            pass
    
    def reset_stats(self):
        """Reseta estatísticas"""
        self.stats = self._load_stats()
        if os.path.exists(self.stats_path):
            os.remove(self.stats_path)


class GlobalStatsCollector:
    """
    Coletor de estatísticas globais
    (Para uso em servidor/dashboard)
    """
    
    def __init__(self, stats_file: str = "global_stats.json"):
        self.stats_file = stats_file
        self.global_stats = self._load_global_stats()
    
    def _load_global_stats(self) -> Dict:
        """Carrega estatísticas globais"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "total_users": 0,
            "active_users_30d": 0,
            "total_backups": 0,
            "total_terabytes": 0.0,
            "total_files": 0,
            "formats": {
                "zip": 0,
                "7z": 0,
                "tar.gz": 0,
                "tar.bz2": 0
            },
            "users": {},
            "last_update": None
        }
    
    def _save_global_stats(self):
        """Salva estatísticas globais"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.global_stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar estatísticas globais: {e}")
    
    def add_user_stats(self, user_token: str, user_stats: Dict):
        """
        Adiciona estatísticas de um usuário
        
        Args:
            user_token: Token único do usuário (hash)
            user_stats: Estatísticas do usuário
        """
        # Hash do token para anonimização
        user_hash = hashlib.sha256(user_token.encode()).hexdigest()[:16]
        
        # Atualiza ou adiciona usuário
        if user_hash not in self.global_stats["users"]:
            self.global_stats["total_users"] += 1
        
        self.global_stats["users"][user_hash] = {
            "total_backups": user_stats.get("total_backups", 0),
            "total_tb": round(user_stats.get("total_bytes_original", 0) / (1024**4), 2),
            "last_backup": user_stats.get("last_backup"),
            "version": user_stats.get("version", "1.0.0")
        }
        
        # Recalcula totais
        self._recalculate_totals()
        
        # Salva
        self.global_stats["last_update"] = datetime.now().isoformat()
        self._save_global_stats()
    
    def _recalculate_totals(self):
        """Recalcula totais agregados"""
        total_backups = 0
        total_tb = 0.0
        active_30d = 0
        
        cutoff_date = datetime.now().timestamp() - (30 * 24 * 60 * 60)
        
        for user_hash, user_data in self.global_stats["users"].items():
            total_backups += user_data.get("total_backups", 0)
            total_tb += user_data.get("total_tb", 0.0)
            
            # Verifica se ativo nos últimos 30 dias
            last_backup = user_data.get("last_backup")
            if last_backup:
                try:
                    last_date = datetime.fromisoformat(last_backup).timestamp()
                    if last_date >= cutoff_date:
                        active_30d += 1
                except:
                    pass
        
        self.global_stats["total_backups"] = total_backups
        self.global_stats["total_terabytes"] = round(total_tb, 2)
        self.global_stats["active_users_30d"] = active_30d
    
    def get_global_stats(self) -> Dict:
        """Retorna estatísticas globais"""
        return {
            "total_users": self.global_stats["total_users"],
            "active_users_30d": self.global_stats["active_users_30d"],
            "total_backups": self.global_stats["total_backups"],
            "total_terabytes": self.global_stats["total_terabytes"],
            "formats": self.global_stats["formats"],
            "last_update": self.global_stats["last_update"]
        }
    
    def generate_dashboard_html(self, output_file: str = "dashboard.html"):
        """Gera dashboard HTML com estatísticas"""
        stats = self.get_global_stats()
        
        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BackupMaster - Estatísticas Globais</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            min-height: 100vh;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        h1 {{
            text-align: center;
            font-size: 3em;
            margin-bottom: 10px;
            color: #ff6b35;
        }}
        
        .subtitle {{
            text-align: center;
            color: #aaa;
            margin-bottom: 50px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
        }}
        
        .stat-card {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 107, 53, 0.3);
            transition: transform 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            border-color: #ff6b35;
        }}
        
        .stat-value {{
            font-size: 3em;
            font-weight: bold;
            color: #ff6b35;
            margin: 10px 0;
        }}
        
        .stat-label {{
            font-size: 1.2em;
            color: #aaa;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 50px;
            color: #666;
        }}
        
        .update-time {{
            text-align: center;
            color: #888;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔄 BackupMaster</h1>
        <p class="subtitle">Estatísticas Globais de Uso</p>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total de Usuários</div>
                <div class="stat-value">{stats['total_users']:,}</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Usuários Ativos (30d)</div>
                <div class="stat-value">{stats['active_users_30d']:,}</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Total de Backups</div>
                <div class="stat-value">{stats['total_backups']:,}</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Terabytes Backupeados</div>
                <div class="stat-value">{stats['total_terabytes']:,.2f} TB</div>
            </div>
        </div>
        
        <p class="update-time">
            Última atualização: {stats['last_update'] or 'N/A'}
        </p>
        
        <div class="footer">
            <p>BackupMaster v1.0.0 - Sistema Profissional de Backup</p>
            <p>100% Gratuito e Open Source</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_file


def format_bytes(bytes_value: int) -> str:
    """Formata bytes para formato legível"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} EB"
