"""
Diálogo de Configurações do BackupMaster
Interface para configurar estratégias de arquivos bloqueados e outras opções
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QCheckBox, QSpinBox, QDoubleSpinBox, QGroupBox,
    QFormLayout, QTabWidget, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from backupmaster.config import (
    ConfigManager, LockedFileStrategy, BackupPreset, get_config_manager
)


class SettingsDialog(QDialog):
    """Diálogo de configurações"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = get_config_manager()
        
        self.setWindowTitle("Configurações - BackupMaster")
        self.setMinimumSize(600, 500)
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Configura interface"""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("⚙️ Configurações")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(header)
        
        # Tabs
        tabs = QTabWidget()
        
        # Tab 1: Arquivos Bloqueados
        locked_files_tab = self.create_locked_files_tab()
        tabs.addTab(locked_files_tab, "🔒 Arquivos Bloqueados")
        
        # Tab 2: Backup
        backup_tab = self.create_backup_tab()
        tabs.addTab(backup_tab, "💾 Backup")
        
        # Tab 3: Interface
        ui_tab = self.create_ui_tab()
        tabs.addTab(ui_tab, "🎨 Interface")
        
        layout.addWidget(tabs)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        # Presets
        preset_label = QLabel("Preset:")
        buttons_layout.addWidget(preset_label)
        
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(["Rápido", "Balanceado", "Completo"])
        self.preset_combo.currentTextChanged.connect(self.apply_preset)
        buttons_layout.addWidget(self.preset_combo)
        
        buttons_layout.addStretch()
        
        # Restaurar padrões
        reset_btn = QPushButton("🔄 Restaurar Padrões")
        reset_btn.clicked.connect(self.reset_defaults)
        buttons_layout.addWidget(reset_btn)
        
        # Salvar
        save_btn = QPushButton("💾 Salvar")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setMinimumHeight(40)
        buttons_layout.addWidget(save_btn)
        
        # Cancelar
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setMinimumHeight(40)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def create_locked_files_tab(self) -> QWidget:
        """Cria tab de arquivos bloqueados"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Grupo: Estratégia
        strategy_group = QGroupBox("Estratégia de Arquivos Bloqueados")
        strategy_layout = QFormLayout()
        
        # Estratégia principal
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems([
            "Automático (Recomendado)",
            "Pular Arquivos Bloqueados",
            "Tentar Novamente",
            "Modo Compartilhado",
            "Volume Shadow Copy (VSS)"
        ])
        strategy_layout.addRow("Estratégia:", self.strategy_combo)
        
        # Max retries
        self.max_retries_spin = QSpinBox()
        self.max_retries_spin.setRange(1, 10)
        self.max_retries_spin.setValue(3)
        strategy_layout.addRow("Tentativas:", self.max_retries_spin)
        
        # Retry delay
        self.retry_delay_spin = QDoubleSpinBox()
        self.retry_delay_spin.setRange(0.1, 5.0)
        self.retry_delay_spin.setSingleStep(0.1)
        self.retry_delay_spin.setValue(0.5)
        self.retry_delay_spin.setSuffix(" s")
        strategy_layout.addRow("Delay entre tentativas:", self.retry_delay_spin)
        
        strategy_group.setLayout(strategy_layout)
        layout.addWidget(strategy_group)
        
        # Grupo: Opções Avançadas
        advanced_group = QGroupBox("Opções Avançadas")
        advanced_layout = QVBoxLayout()
        
        self.use_shared_mode_check = QCheckBox("Usar modo de leitura compartilhada")
        self.use_shared_mode_check.setChecked(True)
        self.use_shared_mode_check.setToolTip("Permite ler arquivos abertos por outros processos")
        advanced_layout.addWidget(self.use_shared_mode_check)
        
        self.use_vss_check = QCheckBox("Usar Volume Shadow Copy (VSS) - Windows")
        self.use_vss_check.setToolTip("Copia de snapshot do volume (requer admin)")
        advanced_layout.addWidget(self.use_vss_check)
        
        self.skip_system_files_check = QCheckBox("Pular arquivos do sistema automaticamente")
        self.skip_system_files_check.setChecked(True)
        self.skip_system_files_check.setToolTip("Pula pagefile.sys, hiberfil.sys, etc")
        advanced_layout.addWidget(self.skip_system_files_check)
        
        self.log_skipped_check = QCheckBox("Registrar arquivos pulados em log")
        self.log_skipped_check.setChecked(True)
        advanced_layout.addWidget(self.log_skipped_check)
        
        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)
        
        # Descrição
        desc_label = QLabel(
            "💡 Dica: Use 'Automático' para melhor compatibilidade.\n"
            "VSS requer privilégios de administrador no Windows."
        )
        desc_label.setStyleSheet("color: gray; font-style: italic;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_backup_tab(self) -> QWidget:
        """Cria tab de configurações de backup"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Grupo: Padrões
        defaults_group = QGroupBox("Configurações Padrão")
        defaults_layout = QFormLayout()
        
        # Formato padrão
        self.default_format_combo = QComboBox()
        self.default_format_combo.addItems(["ZIP", "TAR.GZ", "TAR.BZ2", "7z"])
        defaults_layout.addRow("Formato padrão:", self.default_format_combo)
        
        # Nível de compressão
        self.compression_level_spin = QSpinBox()
        self.compression_level_spin.setRange(0, 9)
        self.compression_level_spin.setValue(6)
        self.compression_level_spin.setToolTip("0 = Sem compressão, 9 = Máxima compressão")
        defaults_layout.addRow("Nível de compressão:", self.compression_level_spin)
        
        defaults_group.setLayout(defaults_layout)
        layout.addWidget(defaults_group)
        
        # Grupo: Opções
        options_group = QGroupBox("Opções")
        options_layout = QVBoxLayout()
        
        self.incremental_default_check = QCheckBox("Backup incremental por padrão")
        options_layout.addWidget(self.incremental_default_check)
        
        self.verify_backup_check = QCheckBox("Verificar backup após criação")
        self.verify_backup_check.setToolTip("Valida integridade do arquivo criado")
        options_layout.addWidget(self.verify_backup_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_ui_tab(self) -> QWidget:
        """Cria tab de configurações de interface"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Grupo: Notificações
        notif_group = QGroupBox("Notificações")
        notif_layout = QVBoxLayout()
        
        self.show_notifications_check = QCheckBox("Mostrar notificações")
        self.show_notifications_check.setChecked(True)
        notif_layout.addWidget(self.show_notifications_check)
        
        notif_group.setLayout(notif_layout)
        layout.addWidget(notif_group)
        
        # Grupo: Comportamento
        behavior_group = QGroupBox("Comportamento")
        behavior_layout = QVBoxLayout()
        
        self.minimize_to_tray_check = QCheckBox("Minimizar para bandeja do sistema")
        self.minimize_to_tray_check.setChecked(True)
        behavior_layout.addWidget(self.minimize_to_tray_check)
        
        self.start_minimized_check = QCheckBox("Iniciar minimizado")
        behavior_layout.addWidget(self.start_minimized_check)
        
        behavior_group.setLayout(behavior_layout)
        layout.addWidget(behavior_group)
        
        # Grupo: Telemetria
        telemetry_group = QGroupBox("Telemetria")
        telemetry_layout = QVBoxLayout()
        
        self.telemetry_enabled_check = QCheckBox("Enviar estatísticas de uso (anônimo)")
        self.telemetry_enabled_check.setChecked(True)
        self.telemetry_enabled_check.setToolTip("Ajuda a melhorar o BackupMaster")
        telemetry_layout.addWidget(self.telemetry_enabled_check)
        
        telemetry_group.setLayout(telemetry_layout)
        layout.addWidget(telemetry_group)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def load_settings(self):
        """Carrega configurações atuais"""
        # Arquivos bloqueados
        strategy = self.config.get('locked_files.strategy')
        strategy_map = {
            'auto': 0,
            'skip': 1,
            'retry': 2,
            'shared_mode': 3,
            'vss': 4
        }
        self.strategy_combo.setCurrentIndex(strategy_map.get(strategy, 0))
        
        self.max_retries_spin.setValue(self.config.get('locked_files.max_retries', 3))
        self.retry_delay_spin.setValue(self.config.get('locked_files.retry_delay', 0.5))
        self.use_shared_mode_check.setChecked(self.config.get('locked_files.use_shared_mode', True))
        self.use_vss_check.setChecked(self.config.get('locked_files.use_vss', False))
        self.skip_system_files_check.setChecked(self.config.get('locked_files.skip_system_files', True))
        self.log_skipped_check.setChecked(self.config.get('locked_files.log_skipped_files', True))
        
        # Backup
        format_map = {'zip': 0, 'tar.gz': 1, 'tar.bz2': 2, '7z': 3}
        default_format = self.config.get('backup.default_format', 'zip')
        self.default_format_combo.setCurrentIndex(format_map.get(default_format, 0))
        
        self.compression_level_spin.setValue(self.config.get('backup.compression_level', 6))
        self.incremental_default_check.setChecked(self.config.get('backup.incremental_by_default', False))
        self.verify_backup_check.setChecked(self.config.get('backup.verify_after_backup', False))
        
        # Interface
        self.show_notifications_check.setChecked(self.config.get('ui.show_notifications', True))
        self.minimize_to_tray_check.setChecked(self.config.get('ui.minimize_to_tray', True))
        self.start_minimized_check.setChecked(self.config.get('ui.start_minimized', False))
        
        # Telemetria
        self.telemetry_enabled_check.setChecked(self.config.get('telemetry.enabled', True))
    
    def save_settings(self):
        """Salva configurações"""
        # Arquivos bloqueados
        strategy_map = {
            0: 'auto',
            1: 'skip',
            2: 'retry',
            3: 'shared_mode',
            4: 'vss'
        }
        
        self.config.set('locked_files.strategy', strategy_map[self.strategy_combo.currentIndex()])
        self.config.set('locked_files.max_retries', self.max_retries_spin.value())
        self.config.set('locked_files.retry_delay', self.retry_delay_spin.value())
        self.config.set('locked_files.use_shared_mode', self.use_shared_mode_check.isChecked())
        self.config.set('locked_files.use_vss', self.use_vss_check.isChecked())
        self.config.set('locked_files.skip_system_files', self.skip_system_files_check.isChecked())
        self.config.set('locked_files.log_skipped_files', self.log_skipped_check.isChecked())
        
        # Backup
        format_map = {0: 'zip', 1: 'tar.gz', 2: 'tar.bz2', 3: '7z'}
        self.config.set('backup.default_format', format_map[self.default_format_combo.currentIndex()])
        self.config.set('backup.compression_level', self.compression_level_spin.value())
        self.config.set('backup.incremental_by_default', self.incremental_default_check.isChecked())
        self.config.set('backup.verify_after_backup', self.verify_backup_check.isChecked())
        
        # Interface
        self.config.set('ui.show_notifications', self.show_notifications_check.isChecked())
        self.config.set('ui.minimize_to_tray', self.minimize_to_tray_check.isChecked())
        self.config.set('ui.start_minimized', self.start_minimized_check.isChecked())
        
        # Telemetria
        self.config.set('telemetry.enabled', self.telemetry_enabled_check.isChecked())
        
        # Salva arquivo
        self.config.save_config()
        
        QMessageBox.information(self, "Sucesso", "Configurações salvas com sucesso!")
        self.accept()
    
    def apply_preset(self, preset_name: str):
        """Aplica preset selecionado"""
        preset_map = {
            "Rápido": BackupPreset.FAST,
            "Balanceado": BackupPreset.BALANCED,
            "Completo": BackupPreset.COMPLETE
        }
        
        if preset_name in preset_map:
            preset = preset_map[preset_name]
            self.config.apply_preset(preset, save=False)
            self.load_settings()
    
    def reset_defaults(self):
        """Restaura configurações padrão"""
        reply = QMessageBox.question(
            self,
            "Confirmar",
            "Restaurar todas as configurações para os valores padrão?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.config.reset_to_defaults(save=False)
            self.load_settings()
            QMessageBox.information(self, "Sucesso", "Configurações restauradas!")
