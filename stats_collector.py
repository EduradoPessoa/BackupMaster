#!/usr/bin/env python3
"""
Script para coletar estatísticas globais de usuários
e gerar dashboard público
"""

import sys
from backupmaster.telemetry import GlobalStatsCollector, TelemetryManager
from backupmaster.auth import LicenseManager


def collect_user_stats():
    """Coleta estatísticas do usuário atual"""
    license_manager = LicenseManager()
    telemetry = TelemetryManager()
    
    if not license_manager.is_registered():
        print("❌ Usuário não registrado. Execute o BackupMaster primeiro.")
        return None
    
    user_info = license_manager.get_user_info()
    user_stats = telemetry.get_stats()
    
    return {
        "token": user_info.get("token"),
        "stats": user_stats
    }


def update_global_stats():
    """Atualiza estatísticas globais"""
    print("📊 Coletando estatísticas globais...")
    
    # Coleta stats do usuário atual
    user_data = collect_user_stats()
    
    if not user_data:
        return
    
    # Atualiza stats globais
    collector = GlobalStatsCollector()
    collector.add_user_stats(user_data["token"], user_data["stats"])
    
    # Mostra estatísticas
    global_stats = collector.get_global_stats()
    
    print("\n" + "="*60)
    print("📈 Estatísticas Globais do BackupMaster")
    print("="*60)
    print(f"\n👥 Total de Usuários: {global_stats['total_users']:,}")
    print(f"🟢 Usuários Ativos (30d): {global_stats['active_users_30d']:,}")
    print(f"📦 Total de Backups: {global_stats['total_backups']:,}")
    print(f"💾 Terabytes Backupeados: {global_stats['total_terabytes']:,.2f} TB")
    print(f"\n⏰ Última Atualização: {global_stats['last_update']}")
    print("="*60 + "\n")
    
    # Gera dashboard HTML
    print("🌐 Gerando dashboard HTML...")
    dashboard_file = collector.generate_dashboard_html()
    print(f"✅ Dashboard gerado: {dashboard_file}")
    print(f"\nAbra o arquivo no navegador para visualizar as estatísticas.\n")


def show_stats():
    """Mostra estatísticas do usuário atual"""
    telemetry = TelemetryManager()
    stats = telemetry.get_formatted_stats()
    
    if stats["total_backups"] == 0:
        print("\n❌ Nenhum backup realizado ainda.\n")
        return
    
    print("\n" + "="*60)
    print("📊 Suas Estatísticas")
    print("="*60)
    print(f"\n📦 Total de Backups: {stats['total_backups']}")
    print(f"📁 Total de Arquivos: {stats['total_files']:,}")
    print(f"💾 Dados Originais: {stats['total_gb_original']:.2f} GB ({stats['total_tb_original']:.3f} TB)")
    print(f"🗜️  Dados Comprimidos: {stats['total_gb_compressed']:.2f} GB ({stats['total_tb_compressed']:.3f} TB)")
    print(f"✨ Espaço Economizado: {stats['total_gb_saved']:.2f} GB ({stats['compression_ratio']:.1f}%)")
    print(f"📅 Dias de Uso: {stats['days_active']} dias")
    
    print(f"\n📦 Backups por Formato:")
    for format_name, count in stats["backups_by_format"].items():
        print(f"  • {format_name.upper()}: {count}")
    
    print(f"\n📈 Detalhes:")
    print(f"  • Backups Completos: {stats['full_backups']}")
    print(f"  • Backups Incrementais: {stats['incremental_backups']}")
    print(f"  • Primeiro Backup: {stats.get('first_backup', 'N/A')}")
    print(f"  • Último Backup: {stats.get('last_backup', 'N/A')}")
    print("="*60 + "\n")


def main():
    """Função principal"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "global":
            update_global_stats()
        elif command == "show":
            show_stats()
        elif command == "help":
            print("""
BackupMaster - Coletor de Estatísticas

Uso:
  python stats_collector.py [comando]

Comandos:
  global    - Atualiza estatísticas globais e gera dashboard
  show      - Mostra suas estatísticas locais
  help      - Mostra esta ajuda

Exemplos:
  python stats_collector.py show
  python stats_collector.py global
""")
        else:
            print(f"❌ Comando desconhecido: {command}")
            print("Use 'python stats_collector.py help' para ver comandos disponíveis.")
    else:
        # Padrão: mostra estatísticas locais
        show_stats()


if __name__ == '__main__':
    main()
