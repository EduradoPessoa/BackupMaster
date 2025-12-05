#!/usr/bin/env python3
"""
BackupMaster CLI - Interface de Linha de Comando
"""

import click
import os
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich import box
from backupmaster.core import BackupEngine
from backupmaster.auth import LicenseManager, check_and_register, show_license_info
from datetime import datetime

console = Console()


def format_size(size_bytes: int) -> str:
    """Formata tamanho em bytes para formato legível"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


@click.group()
@click.version_option(version='1.0.0', prog_name='BackupMaster')
def cli():
    """
    🔄 BackupMaster - Sistema Profissional de Backup
    
    Sistema incremental que só copia arquivos modificados,
    economizando tempo e espaço.
    """
    pass


@cli.command()
@click.option('--source', '-s', required=True, help='Diretório de origem')
@click.option('--dest', '-d', required=True, help='Diretório de destino')
@click.option('--format', '-f', 
              type=click.Choice(['zip', '7z', 'tar.gz', 'tar.bz2']), 
              default='zip',
              help='Formato de compressão')
@click.option('--incremental', '-i', is_flag=True, help='Backup incremental (apenas arquivos modificados)')
@click.option('--name', '-n', help='Nome customizado do backup')
def backup(source, dest, format, incremental, name):
    """Cria um novo backup"""
    
    # Verifica e registra licença se necessário
    license_manager = LicenseManager()
    if not license_manager.is_registered():
        console.print(Panel.fit(
            "[yellow]🔒 Registro Necessário[/yellow]\n\n"
            "[white]O BackupMaster é GRATUITO, mas requer registro.\n"
            "Isso nos ajuda a entender quem está usando o sistema.[/white]",
            title="BackupMaster",
            border_style="yellow"
        ))
        
        name_user = console.input("\n[cyan]Nome:[/cyan] ").strip()
        email = console.input("[cyan]Email:[/cyan] ").strip()
        organization = console.input("[cyan]Organização (opcional):[/cyan] ").strip()
        
        if not name_user or not email:
            console.print("\n[red]❌ Nome e email são obrigatórios![/red]")
            return
        
        result = license_manager.register_user(name_user, email, organization)
        console.print(f"\n[green]✅ {result['message']}[/green]")
        console.print(f"[cyan]🔑 Seu token: {result['token'][:20]}...[/cyan]")
        console.print("\n[yellow]Obrigado por usar o BackupMaster! 🎉[/yellow]\n")
    
    # Valida licença
    if not license_manager.validate_license(offline_mode=True):
        console.print("[red]❌ Erro ao validar licença![/red]")
        return
    
    # Valida diretório de origem
    if not os.path.exists(source):
        console.print(f"[red]❌ Erro: Diretório de origem não encontrado: {source}[/red]")
        return
    
    # Mostra informações
    backup_type = "Incremental" if incremental else "Completo"
    console.print(Panel.fit(
        f"[cyan]Iniciando Backup {backup_type}[/cyan]\n\n"
        f"[white]Origem:[/white] {source}\n"
        f"[white]Destino:[/white] {dest}\n"
        f"[white]Formato:[/white] {format.upper()}",
        title="🔄 BackupMaster",
        border_style="cyan"
    ))
    
    # Cria engine de backup
    engine = BackupEngine()
    
    # Progress tracking
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task("[cyan]Processando...", total=100)
        
        def update_progress(percentage, message):
            progress.update(task, completed=percentage, description=f"[cyan]{message}")
        
        engine.set_progress_callback(update_progress)
        
        try:
            result = engine.create_backup(
                source_dir=source,
                dest_dir=dest,
                format=format,
                incremental=incremental,
                backup_name=name
            )
            
            if result["status"] == "skipped":
                console.print(f"\n[yellow]ℹ️  {result['message']}[/yellow]")
            else:
                # Mostra resultado
                console.print(f"\n[green]✅ Backup concluído com sucesso![/green]\n")
                
                table = Table(show_header=False, box=box.ROUNDED)
                table.add_column("Campo", style="cyan")
                table.add_column("Valor", style="white")
                
                table.add_row("📁 Arquivo", result["filename"])
                table.add_row("📊 Arquivos", str(result["files_count"]))
                table.add_row("📦 Tamanho Original", format_size(result["original_size"]))
                table.add_row("🗜️  Tamanho Comprimido", format_size(result["compressed_size"]))
                table.add_row("💾 Economia de Espaço", f"{result['compression_ratio']:.1f}%")
                table.add_row("🕐 Data/Hora", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                
                console.print(table)
                
        except Exception as e:
            console.print(f"\n[red]❌ Erro ao criar backup: {str(e)}[/red]")


@cli.command()
@click.option('--dest', '-d', required=True, help='Diretório de backups')
def list(dest):
    """Lista todos os backups disponíveis"""
    
    if not os.path.exists(dest):
        console.print(f"[red]❌ Erro: Diretório não encontrado: {dest}[/red]")
        return
    
    engine = BackupEngine()
    backups = engine.list_backups(dest)
    
    if not backups:
        console.print("[yellow]ℹ️  Nenhum backup encontrado[/yellow]")
        return
    
    console.print(Panel.fit(
        f"[cyan]Backups Disponíveis[/cyan]\n\n"
        f"[white]Diretório:[/white] {dest}\n"
        f"[white]Total:[/white] {len(backups)} backup(s)",
        title="📋 Lista de Backups",
        border_style="cyan"
    ))
    
    table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
    table.add_column("📁 Arquivo", style="white")
    table.add_column("📊 Tipo", style="yellow")
    table.add_column("🗜️  Formato", style="magenta")
    table.add_column("📦 Arquivos", justify="right", style="green")
    table.add_column("💾 Economia", justify="right", style="cyan")
    table.add_column("🕐 Data/Hora", style="blue")
    
    for backup in backups:
        backup_type = "Incremental" if backup.get("incremental") else "Completo"
        timestamp = backup.get("timestamp", "")
        
        # Formata timestamp
        try:
            dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
            formatted_date = dt.strftime("%d/%m/%Y %H:%M")
        except:
            formatted_date = timestamp
        
        table.add_row(
            backup.get("filename", ""),
            backup_type,
            backup.get("format", "").upper(),
            str(backup.get("files_count", 0)),
            f"{backup.get('compression_ratio', 0):.1f}%",
            formatted_date
        )
    
    console.print("\n")
    console.print(table)


@cli.command()
@click.option('--backup', '-b', required=True, help='Arquivo de backup')
@click.option('--dest', '-d', required=True, help='Diretório de destino para restauração')
def restore(backup, dest):
    """Restaura um backup"""
    
    if not os.path.exists(backup):
        console.print(f"[red]❌ Erro: Arquivo de backup não encontrado: {backup}[/red]")
        return
    
    console.print(Panel.fit(
        f"[cyan]Restaurando Backup[/cyan]\n\n"
        f"[white]Backup:[/white] {backup}\n"
        f"[white]Destino:[/white] {dest}",
        title="🔄 BackupMaster",
        border_style="cyan"
    ))
    
    engine = BackupEngine()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task("[cyan]Restaurando...", total=100)
        
        def update_progress(percentage, message):
            progress.update(task, completed=percentage, description=f"[cyan]{message}")
        
        engine.set_progress_callback(update_progress)
        
        try:
            result = engine.restore_backup(backup, dest)
            console.print(f"\n[green]✅ {result['message']}[/green]")
            
        except Exception as e:
            console.print(f"\n[red]❌ Erro ao restaurar backup: {str(e)}[/red]")


@cli.command()
def info():
    """Mostra informações sobre o BackupMaster"""
    
    info_text = """
[cyan]🔄 BackupMaster v1.0.0[/cyan]

[white]Sistema Profissional de Backup[/white]

[yellow]Características:[/yellow]
  ✅ Backup Inteligente - Sistema incremental
  ✅ Multi-Plataforma - Windows, Linux e Mac
  ✅ 100% Gratuito - Software livre e open source
  ✅ Múltiplos Formatos - ZIP, 7z, TAR.GZ, TAR.BZ2

[yellow]Formatos Suportados:[/yellow]
  • ZIP     - Compatibilidade universal
  • 7z      - Máxima compressão
  • TAR.GZ  - Padrão Linux/Unix
  • TAR.BZ2 - Alta compressão

[yellow]Exemplos de Uso:[/yellow]
  # Backup completo em ZIP
  backupmaster backup -s "C:/Documentos" -d "D:/Backups" -f zip

  # Backup incremental em 7z
  backupmaster backup -s "C:/Documentos" -d "D:/Backups" -f 7z -i

  # Listar backups
  backupmaster list -d "D:/Backups"

  # Restaurar backup
  backupmaster restore -b "backup.7z" -d "C:/Restaurar"
"""
    
    console.print(Panel(info_text, border_style="cyan", box=box.DOUBLE))


@cli.command()
def license():
    """Mostra informações da licença"""
    show_license_info()


if __name__ == '__main__':
    cli()

