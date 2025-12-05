#!/usr/bin/env python3
"""
BackupMaster GUI - Interface Gráfica com System Tray
"""

import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QProgressBar,
    QFileDialog, QTableWidget, QTableWidgetItem, QCheckBox,
    QSystemTrayIcon, QMenu, QMessageBox, QTextEdit, QGroupBox,
    QHeaderView, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QPixmap, QAction, QPalette, QColor, QFont
import io
from PIL import Image, ImageDraw
from backupmaster.core import BackupEngine
from backupmaster.auth import LicenseManager


class BackupThread(QThread):
    """Thread para executar backup em background"""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, engine, source, dest, format, incremental, name=None):
        super().__init__()
        self.engine = engine
        self.source = source
        self.dest = dest
        self.format = format
        self.incremental = incremental
        self.name = name
    
    def run(self):
        try:
            self.engine.set_progress_callback(self.progress.emit)
            result = self.engine.create_backup(
                source_dir=self.source,
                dest_dir=self.dest,
                format=self.format,
                incremental=self.incremental,
                backup_name=self.name
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class RestoreThread(QThread):
    """Thread para executar restauração em background"""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, engine, backup_file, restore_dir):
        super().__init__()
        self.engine = engine
        self.backup_file = backup_file
        self.restore_dir = restore_dir
    
    def run(self):
        try:
            self.engine.set_progress_callback(self.progress.emit)
            result = self.engine.restore_backup(self.backup_file, self.restore_dir)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class RegistrationDialog(QDialog):
    """Diálogo de registro de usuário"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("BackupMaster - Registro")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        # Estilo
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
            }
            QLabel {
                color: white;
                font-size: 11pt;
            }
            QLineEdit {
                background-color: #0f3460;
                border: 2px solid #16213e;
                border-radius: 6px;
                padding: 10px;
                color: white;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border: 2px solid #ff6b35;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff6b35, stop:1 #f7931e);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f7931e, stop:1 #ff6b35);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Título
        title = QLabel("🔒 Registro Necessário")
        title.setStyleSheet("font-size: 20pt; font-weight: bold; color: #ff6b35;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Descrição
        desc = QLabel(
            "O BackupMaster é GRATUITO, mas requer registro.\n"
            "Isso nos ajuda a entender quem está usando o sistema."
        )
        desc.setStyleSheet("font-size: 10pt; color: #aaaaaa;")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        layout.addSpacing(20)
        
        # Campos
        layout.addWidget(QLabel("Nome:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Seu nome completo")
        layout.addWidget(self.name_input)
        
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("seu@email.com")
        layout.addWidget(self.email_input)
        
        layout.addWidget(QLabel("Organização (opcional):"))
        self.org_input = QLineEdit()
        self.org_input.setPlaceholderText("Empresa ou projeto")
        layout.addWidget(self.org_input)
        
        layout.addSpacing(20)
        
        # Botões
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_data(self):
        """Retorna dados do formulário"""
        return {
            "name": self.name_input.text().strip(),
            "email": self.email_input.text().strip(),
            "organization": self.org_input.text().strip()
        }


class BackupMasterGUI(QMainWindow):
    """Janela principal do BackupMaster"""
    
    def __init__(self):
        super().__init__()
        self.engine = BackupEngine()
        self.backup_thread = None
        self.restore_thread = None
        self.license_manager = LicenseManager()
        
        # Verifica licença antes de inicializar UI
        if not self.check_license():
            sys.exit(0)
        
        self.init_ui()
        self.setup_tray()
    
    def check_license(self) -> bool:
        """Verifica e registra licença se necessário"""
        if self.license_manager.is_registered():
            # Valida licença existente
            if self.license_manager.validate_license(offline_mode=True):
                return True
            else:
                QMessageBox.critical(
                    None,
                    "Erro",
                    "Licença inválida. Por favor, registre-se novamente."
                )
                self.license_manager.revoke_license()
                return self.check_license()
        
        # Mostra diálogo de registro
        dialog = RegistrationDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            
            if not data["name"] or not data["email"]:
                QMessageBox.warning(
                    None,
                    "Aviso",
                    "Nome e email são obrigatórios!"
                )
                return self.check_license()
            
            # Registra usuário
            result = self.license_manager.register_user(
                data["name"],
                data["email"],
                data["organization"]
            )
            
            QMessageBox.information(
                None,
                "Sucesso",
                f"{result['message']}\n\n"
                f"Seu token: {result['token'][:20]}...\n\n"
                "Obrigado por usar o BackupMaster! 🎉"
            )
            
            return True
        else:
            return False
        
    def init_ui(self):
        """Inicializa interface do usuário"""
        self.setWindowTitle("BackupMaster - Sistema Profissional de Backup")
        self.setGeometry(100, 100, 900, 700)
        
        # Define estilo moderno
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
            }
            QWidget {
                background-color: transparent;
                color: #ffffff;
                font-family: 'Segoe UI', Arial;
                font-size: 10pt;
            }
            QGroupBox {
                border: 2px solid #ff6b35;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
                color: #ff6b35;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff6b35, stop:1 #f7931e);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f7931e, stop:1 #ff6b35);
            }
            QPushButton:pressed {
                background: #e85d04;
            }
            QPushButton:disabled {
                background: #555555;
                color: #888888;
            }
            QLineEdit, QComboBox {
                background-color: #0f3460;
                border: 2px solid #16213e;
                border-radius: 6px;
                padding: 8px;
                color: white;
                selection-background-color: #ff6b35;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #ff6b35;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ff6b35;
                margin-right: 5px;
            }
            QProgressBar {
                border: 2px solid #16213e;
                border-radius: 8px;
                text-align: center;
                background-color: #0f3460;
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff6b35, stop:1 #f7931e);
                border-radius: 6px;
            }
            QTableWidget {
                background-color: #0f3460;
                border: 2px solid #16213e;
                border-radius: 8px;
                gridline-color: #16213e;
                color: white;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #ff6b35;
            }
            QHeaderView::section {
                background-color: #16213e;
                color: #ff6b35;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QCheckBox {
                spacing: 8px;
                color: white;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #ff6b35;
                border-radius: 4px;
                background-color: #0f3460;
            }
            QCheckBox::indicator:checked {
                background-color: #ff6b35;
                image: none;
            }
            QTextEdit {
                background-color: #0f3460;
                border: 2px solid #16213e;
                border-radius: 8px;
                padding: 8px;
                color: #00ff00;
                font-family: 'Consolas', monospace;
            }
            QLabel {
                color: white;
            }
        """)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("🔄 BackupMaster")
        header.setStyleSheet("""
            font-size: 28pt;
            font-weight: bold;
            color: #ff6b35;
            padding: 10px;
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        
        subtitle = QLabel("Sistema Profissional de Backup")
        subtitle.setStyleSheet("""
            font-size: 12pt;
            color: #aaaaaa;
            padding-bottom: 10px;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle)
        
        # Grupo de Configuração de Backup
        backup_group = QGroupBox("⚙️ Configuração de Backup")
        backup_layout = QVBoxLayout()
        backup_layout.setSpacing(10)
        
        # Diretório de origem
        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel("📁 Origem:"))
        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText("Selecione o diretório de origem...")
        source_layout.addWidget(self.source_input)
        source_btn = QPushButton("Procurar")
        source_btn.clicked.connect(self.select_source)
        source_layout.addWidget(source_btn)
        backup_layout.addLayout(source_layout)
        
        # Diretório de destino
        dest_layout = QHBoxLayout()
        dest_layout.addWidget(QLabel("💾 Destino:"))
        self.dest_input = QLineEdit()
        self.dest_input.setPlaceholderText("Selecione o diretório de destino...")
        dest_layout.addWidget(self.dest_input)
        dest_btn = QPushButton("Procurar")
        dest_btn.clicked.connect(self.select_dest)
        dest_layout.addWidget(dest_btn)
        backup_layout.addLayout(dest_layout)
        
        # Formato e opções
        options_layout = QHBoxLayout()
        options_layout.addWidget(QLabel("🗜️ Formato:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(['ZIP', '7z', 'TAR.GZ', 'TAR.BZ2'])
        options_layout.addWidget(self.format_combo)
        
        self.incremental_check = QCheckBox("📊 Backup Incremental")
        self.incremental_check.setToolTip("Copia apenas arquivos modificados")
        options_layout.addWidget(self.incremental_check)
        options_layout.addStretch()
        backup_layout.addLayout(options_layout)
        
        backup_group.setLayout(backup_layout)
        main_layout.addWidget(backup_group)
        
        # Botão de Backup
        self.backup_btn = QPushButton("🚀 Iniciar Backup")
        self.backup_btn.setMinimumHeight(50)
        self.backup_btn.clicked.connect(self.start_backup)
        main_layout.addWidget(self.backup_btn)
        
        # Barra de progresso
        progress_group = QGroupBox("📈 Progresso")
        progress_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(30)
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Aguardando...")
        self.status_label.setStyleSheet("color: #aaaaaa; font-style: italic;")
        progress_layout.addWidget(self.status_label)
        
        progress_group.setLayout(progress_layout)
        main_layout.addWidget(progress_group)
        
        # Tabela de backups
        history_group = QGroupBox("📋 Histórico de Backups")
        history_layout = QVBoxLayout()
        
        self.backup_table = QTableWidget()
        self.backup_table.setColumnCount(5)
        self.backup_table.setHorizontalHeaderLabels([
            "Arquivo", "Tipo", "Formato", "Arquivos", "Economia"
        ])
        self.backup_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.backup_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.backup_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        history_layout.addWidget(self.backup_table)
        
        # Botões de ação
        action_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 Atualizar Lista")
        refresh_btn.clicked.connect(self.refresh_backup_list)
        action_layout.addWidget(refresh_btn)
        
        restore_btn = QPushButton("📥 Restaurar Selecionado")
        restore_btn.clicked.connect(self.restore_selected)
        action_layout.addWidget(restore_btn)
        
        history_layout.addLayout(action_layout)
        history_group.setLayout(history_layout)
        main_layout.addWidget(history_group)
        
    def setup_tray(self):
        """Configura ícone na bandeja do sistema"""
        # Cria ícone
        icon = self.create_tray_icon()
        
        self.tray_icon = QSystemTrayIcon(icon, self)
        
        # Menu do tray
        tray_menu = QMenu()
        
        show_action = QAction("Mostrar", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        hide_action = QAction("Minimizar", self)
        hide_action.triggered.connect(self.hide)
        tray_menu.addAction(hide_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("Sair", self)
        quit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
        
        # Mensagem inicial
        self.tray_icon.showMessage(
            "BackupMaster",
            "Sistema de backup iniciado",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )
    
    def create_tray_icon(self):
        """Cria ícone para a bandeja do sistema"""
        # Cria imagem do ícone
        img = Image.new('RGB', (64, 64), color='#ff6b35')
        draw = ImageDraw.Draw(img)
        
        # Desenha círculo
        draw.ellipse([8, 8, 56, 56], fill='#ff6b35', outline='white', width=3)
        
        # Converte para QPixmap
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.read())
        
        return QIcon(pixmap)
    
    def tray_icon_activated(self, reason):
        """Callback quando ícone do tray é ativado"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.activateWindow()
    
    def closeEvent(self, event):
        """Minimiza para tray ao invés de fechar"""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "BackupMaster",
            "Aplicativo minimizado para a bandeja",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )
    
    def select_source(self):
        """Seleciona diretório de origem"""
        dir_path = QFileDialog.getExistingDirectory(self, "Selecionar Diretório de Origem")
        if dir_path:
            self.source_input.setText(dir_path)
    
    def select_dest(self):
        """Seleciona diretório de destino"""
        dir_path = QFileDialog.getExistingDirectory(self, "Selecionar Diretório de Destino")
        if dir_path:
            self.dest_input.setText(dir_path)
            self.refresh_backup_list()
    
    def start_backup(self):
        """Inicia processo de backup"""
        source = self.source_input.text()
        dest = self.dest_input.text()
        
        if not source or not dest:
            QMessageBox.warning(self, "Aviso", "Selecione os diretórios de origem e destino!")
            return
        
        if not os.path.exists(source):
            QMessageBox.critical(self, "Erro", f"Diretório de origem não encontrado:\n{source}")
            return
        
        # Desabilita botão
        self.backup_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_label.setText("Iniciando backup...")
        
        # Inicia thread de backup
        format_map = {
            'ZIP': 'zip',
            '7z': '7z',
            'TAR.GZ': 'tar.gz',
            'TAR.BZ2': 'tar.bz2'
        }
        
        self.backup_thread = BackupThread(
            self.engine,
            source,
            dest,
            format_map[self.format_combo.currentText()],
            self.incremental_check.isChecked()
        )
        
        self.backup_thread.progress.connect(self.update_progress)
        self.backup_thread.finished.connect(self.backup_finished)
        self.backup_thread.error.connect(self.backup_error)
        self.backup_thread.start()
    
    def update_progress(self, percentage, message):
        """Atualiza barra de progresso"""
        self.progress_bar.setValue(percentage)
        self.status_label.setText(message)
    
    def backup_finished(self, result):
        """Callback quando backup termina"""
        self.backup_btn.setEnabled(True)
        
        if result["status"] == "skipped":
            QMessageBox.information(self, "Informação", result["message"])
        else:
            # Mostra mensagem de sucesso
            msg = f"""Backup concluído com sucesso!

Arquivo: {result['filename']}
Arquivos: {result['files_count']}
Economia de espaço: {result['compression_ratio']:.1f}%"""
            
            QMessageBox.information(self, "Sucesso", msg)
            
            # Notificação no tray
            self.tray_icon.showMessage(
                "Backup Concluído",
                f"{result['files_count']} arquivos - {result['compression_ratio']:.1f}% economia",
                QSystemTrayIcon.MessageIcon.Information,
                3000
            )
        
        self.refresh_backup_list()
    
    def backup_error(self, error_msg):
        """Callback quando ocorre erro no backup"""
        self.backup_btn.setEnabled(True)
        QMessageBox.critical(self, "Erro", f"Erro ao criar backup:\n{error_msg}")
    
    def refresh_backup_list(self):
        """Atualiza lista de backups"""
        dest = self.dest_input.text()
        if not dest or not os.path.exists(dest):
            return
        
        backups = self.engine.list_backups(dest)
        
        self.backup_table.setRowCount(len(backups))
        
        for i, backup in enumerate(backups):
            self.backup_table.setItem(i, 0, QTableWidgetItem(backup.get("filename", "")))
            
            backup_type = "Incremental" if backup.get("incremental") else "Completo"
            self.backup_table.setItem(i, 1, QTableWidgetItem(backup_type))
            
            self.backup_table.setItem(i, 2, QTableWidgetItem(backup.get("format", "").upper()))
            self.backup_table.setItem(i, 3, QTableWidgetItem(str(backup.get("files_count", 0))))
            self.backup_table.setItem(i, 4, QTableWidgetItem(f"{backup.get('compression_ratio', 0):.1f}%"))
    
    def restore_selected(self):
        """Restaura backup selecionado"""
        selected_rows = self.backup_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "Aviso", "Selecione um backup para restaurar!")
            return
        
        row = selected_rows[0].row()
        filename = self.backup_table.item(row, 0).text()
        
        dest = self.dest_input.text()
        backup_file = os.path.join(dest, filename)
        
        # Seleciona diretório de restauração
        restore_dir = QFileDialog.getExistingDirectory(self, "Selecionar Diretório de Restauração")
        if not restore_dir:
            return
        
        # Confirma restauração
        reply = QMessageBox.question(
            self,
            "Confirmar Restauração",
            f"Restaurar backup:\n{filename}\n\nPara:\n{restore_dir}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.No:
            return
        
        # Inicia thread de restauração
        self.backup_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_label.setText("Restaurando backup...")
        
        self.restore_thread = RestoreThread(self.engine, backup_file, restore_dir)
        self.restore_thread.progress.connect(self.update_progress)
        self.restore_thread.finished.connect(self.restore_finished)
        self.restore_thread.error.connect(self.restore_error)
        self.restore_thread.start()
    
    def restore_finished(self, result):
        """Callback quando restauração termina"""
        self.backup_btn.setEnabled(True)
        QMessageBox.information(self, "Sucesso", result["message"])
        
        self.tray_icon.showMessage(
            "Restauração Concluída",
            "Backup restaurado com sucesso!",
            QSystemTrayIcon.MessageIcon.Information,
            3000
        )
    
    def restore_error(self, error_msg):
        """Callback quando ocorre erro na restauração"""
        self.backup_btn.setEnabled(True)
        QMessageBox.critical(self, "Erro", f"Erro ao restaurar backup:\n{error_msg}")


def main():
    """Função principal"""
    app = QApplication(sys.argv)
    app.setApplicationName("BackupMaster")
    app.setQuitOnLastWindowClosed(False)  # Não fecha ao minimizar
    
    window = BackupMasterGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
