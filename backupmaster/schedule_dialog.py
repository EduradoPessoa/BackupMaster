"""
Diálogo de Agendamento de Backups
Interface gráfica para criar e gerenciar agendamentos
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QCheckBox, QTimeEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog,
    QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QFont
from backupmaster.scheduler import BackupScheduler


class ScheduleDialog(QDialog):
    """Diálogo para criar/editar agendamento"""
    
    def __init__(self, parent=None, schedule_data=None):
        super().__init__(parent)
        self.schedule_data = schedule_data
        self.is_edit = schedule_data is not None
        
        self.setWindowTitle("Editar Agendamento" if self.is_edit else "Novo Agendamento")
        self.setMinimumWidth(500)
        self.setup_ui()
        
        if self.is_edit:
            self.load_schedule_data()
    
    def setup_ui(self):
        """Configura interface"""
        layout = QVBoxLayout()
        
        # Formulário
        form_group = QGroupBox("Configurações do Backup")
        form_layout = QFormLayout()
        
        # Nome
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ex: Backup Diário Documentos")
        form_layout.addRow("Nome:", self.name_input)
        
        # Origem
        source_layout = QHBoxLayout()
        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText("Selecione a pasta de origem")
        source_btn = QPushButton("📁 Selecionar")
        source_btn.clicked.connect(self.select_source)
        source_layout.addWidget(self.source_input)
        source_layout.addWidget(source_btn)
        form_layout.addRow("Origem:", source_layout)
        
        # Destino
        dest_layout = QHBoxLayout()
        self.dest_input = QLineEdit()
        self.dest_input.setPlaceholderText("Selecione a pasta de destino")
        dest_btn = QPushButton("📁 Selecionar")
        dest_btn.clicked.connect(self.select_destination)
        dest_layout.addWidget(self.dest_input)
        dest_layout.addWidget(dest_btn)
        form_layout.addRow("Destino:", dest_layout)
        
        # Formato
        self.format_combo = QComboBox()
        from backupmaster.core import HAS_7Z
        formats = ['ZIP']
        if HAS_7Z:
            formats.append('7z')
        formats.extend(['TAR.GZ', 'TAR.BZ2'])
        self.format_combo.addItems(formats)
        form_layout.addRow("Formato:", self.format_combo)
        
        # Incremental
        self.incremental_check = QCheckBox("Backup Incremental")
        form_layout.addRow("", self.incremental_check)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Agendamento
        schedule_group = QGroupBox("Agendamento")
        schedule_layout = QFormLayout()
        
        # Frequência
        self.frequency_combo = QComboBox()
        self.frequency_combo.addItems(['Diário', 'Semanal', 'Mensal'])
        schedule_layout.addRow("Frequência:", self.frequency_combo)
        
        # Horário
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime(2, 0))  # 02:00 padrão
        schedule_layout.addRow("Horário:", self.time_edit)
        
        # Ativo
        self.enabled_check = QCheckBox("Agendamento Ativo")
        self.enabled_check.setChecked(True)
        schedule_layout.addRow("", self.enabled_check)
        
        schedule_group.setLayout(schedule_layout)
        layout.addWidget(schedule_group)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Salvar")
        save_btn.clicked.connect(self.accept)
        save_btn.setMinimumHeight(40)
        
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setMinimumHeight(40)
        
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def select_source(self):
        """Seleciona diretório de origem"""
        folder = QFileDialog.getExistingDirectory(self, "Selecionar Pasta de Origem")
        if folder:
            self.source_input.setText(folder)
    
    def select_destination(self):
        """Seleciona diretório de destino"""
        folder = QFileDialog.getExistingDirectory(self, "Selecionar Pasta de Destino")
        if folder:
            self.dest_input.setText(folder)
    
    def load_schedule_data(self):
        """Carrega dados do agendamento para edição"""
        self.name_input.setText(self.schedule_data['name'])
        self.source_input.setText(self.schedule_data['source'])
        self.dest_input.setText(self.schedule_data['destination'])
        
        # Formato
        format_map = {'zip': 'ZIP', '7z': '7z', 'tar.gz': 'TAR.GZ', 'tar.bz2': 'TAR.BZ2'}
        format_text = format_map.get(self.schedule_data['format'], 'ZIP')
        index = self.format_combo.findText(format_text)
        if index >= 0:
            self.format_combo.setCurrentIndex(index)
        
        self.incremental_check.setChecked(self.schedule_data['incremental'])
        
        # Frequência
        freq_map = {'daily': 'Diário', 'weekly': 'Semanal', 'monthly': 'Mensal'}
        freq_text = freq_map.get(self.schedule_data['frequency'], 'Diário')
        index = self.frequency_combo.findText(freq_text)
        if index >= 0:
            self.frequency_combo.setCurrentIndex(index)
        
        # Horário
        hour, minute = map(int, self.schedule_data['time'].split(':'))
        self.time_edit.setTime(QTime(hour, minute))
        
        self.enabled_check.setChecked(self.schedule_data.get('enabled', True))
    
    def get_schedule_data(self):
        """Retorna dados do formulário"""
        format_map = {'ZIP': 'zip', '7z': '7z', 'TAR.GZ': 'tar.gz', 'TAR.BZ2': 'tar.bz2'}
        freq_map = {'Diário': 'daily', 'Semanal': 'weekly', 'Mensal': 'monthly'}
        
        return {
            'name': self.name_input.text(),
            'source': self.source_input.text(),
            'destination': self.dest_input.text(),
            'format': format_map[self.format_combo.currentText()],
            'incremental': self.incremental_check.isChecked(),
            'frequency': freq_map[self.frequency_combo.currentText()],
            'time': self.time_edit.time().toString("HH:mm"),
            'enabled': self.enabled_check.isChecked()
        }


class ScheduleManagerDialog(QDialog):
    """Diálogo para gerenciar todos os agendamentos"""
    
    def __init__(self, scheduler: BackupScheduler, parent=None):
        super().__init__(parent)
        self.scheduler = scheduler
        
        self.setWindowTitle("Gerenciar Agendamentos")
        self.setMinimumSize(800, 500)
        self.setup_ui()
        self.load_schedules()
    
    def setup_ui(self):
        """Configura interface"""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("📅 Agendamentos de Backup")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(header)
        
        # Tabela
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Nome", "Frequência", "Horário", "Formato", "Status", "Próxima Execução", "Ações"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        new_btn = QPushButton("➕ Novo Agendamento")
        new_btn.clicked.connect(self.new_schedule)
        new_btn.setMinimumHeight(40)
        
        close_btn = QPushButton("✅ Fechar")
        close_btn.clicked.connect(self.accept)
        close_btn.setMinimumHeight(40)
        
        buttons_layout.addWidget(new_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def load_schedules(self):
        """Carrega agendamentos na tabela"""
        schedules = self.scheduler.get_all_schedules()
        self.table.setRowCount(len(schedules))
        
        freq_map = {'daily': 'Diário', 'weekly': 'Semanal', 'monthly': 'Mensal'}
        format_map = {'zip': 'ZIP', '7z': '7z', 'tar.gz': 'TAR.GZ', 'tar.bz2': 'TAR.BZ2'}
        
        for row, schedule in enumerate(schedules):
            # Nome
            self.table.setItem(row, 0, QTableWidgetItem(schedule['name']))
            
            # Frequência
            freq_text = freq_map.get(schedule['frequency'], schedule['frequency'])
            self.table.setItem(row, 1, QTableWidgetItem(freq_text))
            
            # Horário
            self.table.setItem(row, 2, QTableWidgetItem(schedule['time']))
            
            # Formato
            format_text = format_map.get(schedule['format'], schedule['format'].upper())
            self.table.setItem(row, 3, QTableWidgetItem(format_text))
            
            # Status
            status = "✅ Ativo" if schedule.get('enabled', True) else "⏸️ Pausado"
            self.table.setItem(row, 4, QTableWidgetItem(status))
            
            # Próxima execução
            next_run = schedule.get('next_run', 'N/A')
            if next_run != 'N/A':
                from datetime import datetime
                try:
                    dt = datetime.fromisoformat(next_run)
                    next_run = dt.strftime("%d/%m/%Y %H:%M")
                except:
                    pass
            self.table.setItem(row, 5, QTableWidgetItem(next_run))
            
            # Botões de ação
            actions_widget = self.create_action_buttons(schedule['id'])
            self.table.setCellWidget(row, 6, actions_widget)
    
    def create_action_buttons(self, schedule_id):
        """Cria botões de ação para cada linha"""
        from PyQt6.QtWidgets import QWidget
        
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        
        edit_btn = QPushButton("✏️")
        edit_btn.setToolTip("Editar")
        edit_btn.setMaximumWidth(40)
        edit_btn.clicked.connect(lambda: self.edit_schedule(schedule_id))
        
        delete_btn = QPushButton("🗑️")
        delete_btn.setToolTip("Excluir")
        delete_btn.setMaximumWidth(40)
        delete_btn.clicked.connect(lambda: self.delete_schedule(schedule_id))
        
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def new_schedule(self):
        """Cria novo agendamento"""
        dialog = ScheduleDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_schedule_data()
            
            # Validações
            if not data['name']:
                QMessageBox.warning(self, "Erro", "Digite um nome para o agendamento")
                return
            
            if not data['source'] or not data['destination']:
                QMessageBox.warning(self, "Erro", "Selecione origem e destino")
                return
            
            # Adiciona agendamento
            self.scheduler.add_schedule(**data)
            self.load_schedules()
            
            QMessageBox.information(self, "Sucesso", "Agendamento criado com sucesso!")
    
    def edit_schedule(self, schedule_id):
        """Edita agendamento existente"""
        schedule_data = self.scheduler.get_schedule(schedule_id)
        if not schedule_data:
            return
        
        dialog = ScheduleDialog(self, schedule_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_schedule_data()
            self.scheduler.update_schedule(schedule_id, **data)
            self.load_schedules()
            
            QMessageBox.information(self, "Sucesso", "Agendamento atualizado!")
    
    def delete_schedule(self, schedule_id):
        """Exclui agendamento"""
        reply = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            "Tem certeza que deseja excluir este agendamento?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.scheduler.delete_schedule(schedule_id)
            self.load_schedules()
            
            QMessageBox.information(self, "Sucesso", "Agendamento excluído!")
