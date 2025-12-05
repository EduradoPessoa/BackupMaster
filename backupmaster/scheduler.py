"""
Sistema de Agendamento de Backups
Permite agendar backups automáticos em horários específicos
"""

import json
import os
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Callable, Optional
import schedule


class BackupScheduler:
    """Gerenciador de agendamentos de backup"""
    
    def __init__(self, config_file: str = None):
        """
        Inicializa o agendador
        
        Args:
            config_file: Caminho para arquivo de configuração dos agendamentos
        """
        if config_file is None:
            config_file = str(Path.home() / ".backupmaster_schedules.json")
        
        self.config_file = config_file
        self.schedules: List[Dict] = []
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.callback: Optional[Callable] = None
        
        self.load_schedules()
    
    def load_schedules(self):
        """Carrega agendamentos do arquivo"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.schedules = json.load(f)
            except Exception as e:
                print(f"Erro ao carregar agendamentos: {e}")
                self.schedules = []
        else:
            self.schedules = []
    
    def save_schedules(self):
        """Salva agendamentos no arquivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.schedules, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar agendamentos: {e}")
    
    def add_schedule(self, name: str, source: str, destination: str, 
                    format: str, incremental: bool, frequency: str, 
                    time_str: str, enabled: bool = True) -> Dict:
        """
        Adiciona um novo agendamento
        
        Args:
            name: Nome do agendamento
            source: Diretório de origem
            destination: Diretório de destino
            format: Formato do backup (zip, 7z, tar.gz, tar.bz2)
            incremental: Se é backup incremental
            frequency: Frequência (daily, weekly, monthly)
            time_str: Horário (HH:MM)
            enabled: Se está ativo
        
        Returns:
            Dicionário com o agendamento criado
        """
        schedule_id = self._generate_id()
        
        schedule_data = {
            'id': schedule_id,
            'name': name,
            'source': source,
            'destination': destination,
            'format': format,
            'incremental': incremental,
            'frequency': frequency,
            'time': time_str,
            'enabled': enabled,
            'created_at': datetime.now().isoformat(),
            'last_run': None,
            'next_run': self._calculate_next_run(frequency, time_str)
        }
        
        self.schedules.append(schedule_data)
        self.save_schedules()
        
        # Recarrega agendamentos se estiver rodando
        if self.running:
            self._setup_schedules()
        
        return schedule_data
    
    def update_schedule(self, schedule_id: str, **kwargs):
        """Atualiza um agendamento existente"""
        for schedule_data in self.schedules:
            if schedule_data['id'] == schedule_id:
                schedule_data.update(kwargs)
                
                # Recalcula próxima execução se mudou frequência ou horário
                if 'frequency' in kwargs or 'time' in kwargs:
                    schedule_data['next_run'] = self._calculate_next_run(
                        schedule_data['frequency'],
                        schedule_data['time']
                    )
                
                self.save_schedules()
                
                if self.running:
                    self._setup_schedules()
                
                return True
        
        return False
    
    def delete_schedule(self, schedule_id: str) -> bool:
        """Remove um agendamento"""
        initial_len = len(self.schedules)
        self.schedules = [s for s in self.schedules if s['id'] != schedule_id]
        
        if len(self.schedules) < initial_len:
            self.save_schedules()
            
            if self.running:
                self._setup_schedules()
            
            return True
        
        return False
    
    def get_schedule(self, schedule_id: str) -> Optional[Dict]:
        """Retorna um agendamento específico"""
        for schedule_data in self.schedules:
            if schedule_data['id'] == schedule_id:
                return schedule_data
        return None
    
    def get_all_schedules(self) -> List[Dict]:
        """Retorna todos os agendamentos"""
        return self.schedules.copy()
    
    def set_callback(self, callback: Callable):
        """
        Define callback para executar backup
        
        Args:
            callback: Função que recebe (source, destination, format, incremental)
        """
        self.callback = callback
    
    def start(self):
        """Inicia o agendador em background"""
        if self.running:
            return
        
        self.running = True
        self._setup_schedules()
        
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Para o agendador"""
        self.running = False
        schedule.clear()
        
        if self.thread:
            self.thread.join(timeout=2)
    
    def _setup_schedules(self):
        """Configura todos os agendamentos ativos"""
        schedule.clear()
        
        for schedule_data in self.schedules:
            if not schedule_data.get('enabled', True):
                continue
            
            frequency = schedule_data['frequency']
            time_str = schedule_data['time']
            
            job = self._create_job(schedule_data)
            
            if frequency == 'daily':
                schedule.every().day.at(time_str).do(job)
            elif frequency == 'weekly':
                # Executa toda segunda-feira
                schedule.every().monday.at(time_str).do(job)
            elif frequency == 'monthly':
                # Executa todo dia 1
                schedule.every().day.at(time_str).do(
                    lambda: job() if datetime.now().day == 1 else None
                )
    
    def _create_job(self, schedule_data: Dict):
        """Cria função de job para um agendamento"""
        def job():
            if not self.callback:
                print(f"Callback não definido para agendamento: {schedule_data['name']}")
                return
            
            try:
                print(f"Executando backup agendado: {schedule_data['name']}")
                
                # Executa callback
                self.callback(
                    schedule_data['source'],
                    schedule_data['destination'],
                    schedule_data['format'],
                    schedule_data['incremental']
                )
                
                # Atualiza última execução
                schedule_data['last_run'] = datetime.now().isoformat()
                schedule_data['next_run'] = self._calculate_next_run(
                    schedule_data['frequency'],
                    schedule_data['time']
                )
                self.save_schedules()
                
                print(f"Backup agendado concluído: {schedule_data['name']}")
                
            except Exception as e:
                print(f"Erro ao executar backup agendado: {e}")
        
        return job
    
    def _run_scheduler(self):
        """Loop principal do agendador"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def _generate_id(self) -> str:
        """Gera ID único para agendamento"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def _calculate_next_run(self, frequency: str, time_str: str) -> str:
        """Calcula próxima execução"""
        try:
            hour, minute = map(int, time_str.split(':'))
            now = datetime.now()
            
            # Cria datetime para hoje no horário especificado
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # Se já passou hoje, agenda para amanhã/próxima ocorrência
            if next_run <= now:
                if frequency == 'daily':
                    next_run += timedelta(days=1)
                elif frequency == 'weekly':
                    # Próxima segunda-feira
                    days_ahead = 0 - now.weekday()
                    if days_ahead <= 0:
                        days_ahead += 7
                    next_run += timedelta(days=days_ahead)
                elif frequency == 'monthly':
                    # Próximo dia 1
                    if now.day == 1:
                        next_run += timedelta(days=30)
                    else:
                        next_month = now.replace(day=1) + timedelta(days=32)
                        next_run = next_month.replace(day=1, hour=hour, minute=minute)
            
            return next_run.isoformat()
        
        except Exception as e:
            print(f"Erro ao calcular próxima execução: {e}")
            return datetime.now().isoformat()
