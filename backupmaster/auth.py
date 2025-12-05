"""
Sistema de Autenticação e Licenciamento do BackupMaster
"""

import os
import json
import uuid
import hashlib
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict


class LicenseManager:
    """Gerenciador de licenças e autenticação"""
    
    # URL do servidor de validação (pode ser GitHub Pages, Firebase, etc.)
    VALIDATION_SERVER = "https://raw.githubusercontent.com/seu-usuario/backupmaster-licenses/main/licenses.json"
    
    # Arquivo local de licença
    LICENSE_FILE = ".backupmaster_license"
    
    def __init__(self):
        self.license_path = self._get_license_path()
        self.user_data = self._load_license()
        
    def _get_license_path(self) -> str:
        """Retorna caminho do arquivo de licença"""
        # Salva na pasta do usuário
        home = Path.home()
        return os.path.join(home, self.LICENSE_FILE)
    
    def _load_license(self) -> Optional[Dict]:
        """Carrega licença local"""
        if os.path.exists(self.license_path):
            try:
                with open(self.license_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao carregar licença: {e}")
        return None
    
    def _save_license(self, data: Dict):
        """Salva licença localmente"""
        try:
            with open(self.license_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar licença: {e}")
    
    def _generate_machine_id(self) -> str:
        """Gera ID único da máquina"""
        # Usa informações do sistema para gerar ID único
        import platform
        import socket
        
        machine_info = f"{platform.node()}-{platform.machine()}-{socket.gethostname()}"
        return hashlib.sha256(machine_info.encode()).hexdigest()[:16]
    
    def _generate_token(self, email: str, name: str) -> str:
        """Gera token único para o usuário"""
        unique_data = f"{email}-{name}-{uuid.uuid4()}"
        return hashlib.sha256(unique_data.encode()).hexdigest()
    
    def register_user(self, name: str, email: str, organization: str = "") -> Dict:
        """
        Registra novo usuário e gera token
        
        Args:
            name: Nome do usuário
            email: Email do usuário
            organization: Organização (opcional)
            
        Returns:
            Dict com informações do registro
        """
        # Gera token único
        token = self._generate_token(email, name)
        machine_id = self._generate_machine_id()
        
        # Dados do usuário
        user_data = {
            "token": token,
            "name": name,
            "email": email,
            "organization": organization,
            "machine_id": machine_id,
            "registered_at": datetime.now().isoformat(),
            "last_validation": datetime.now().isoformat(),
            "version": "1.0.0"
        }
        
        # Salva localmente
        self._save_license(user_data)
        self.user_data = user_data
        
        # Envia para servidor (opcional - pode ser implementado depois)
        self._send_registration(user_data)
        
        return {
            "status": "success",
            "token": token,
            "message": "Registro realizado com sucesso!"
        }
    
    def _send_registration(self, user_data: Dict):
        """
        Envia registro para servidor
        (Implementação opcional - pode usar GitHub Issues, Firebase, etc.)
        """
        try:
            # Exemplo: criar issue no GitHub com os dados
            # Ou enviar para webhook, Firebase, etc.
            
            # Por enquanto, apenas log local
            log_file = os.path.join(Path.home(), ".backupmaster_registrations.log")
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now().isoformat()} - {json.dumps(user_data)}\n")
                
        except Exception as e:
            # Falha silenciosa - não bloqueia o uso
            pass
    
    def validate_license(self, offline_mode: bool = False) -> bool:
        """
        Valida licença do usuário
        
        Args:
            offline_mode: Se True, valida apenas localmente
            
        Returns:
            True se licença válida, False caso contrário
        """
        # Verifica se existe licença local
        if not self.user_data:
            return False
        
        # Validação offline (sempre permitida)
        if offline_mode or not self._has_internet():
            return self._validate_offline()
        
        # Validação online (opcional)
        return self._validate_online()
    
    def _has_internet(self) -> bool:
        """Verifica se tem conexão com internet"""
        try:
            requests.get("https://www.google.com", timeout=2)
            return True
        except:
            return False
    
    def _validate_offline(self) -> bool:
        """Validação offline - verifica apenas estrutura local"""
        required_fields = ["token", "name", "email", "registered_at"]
        
        for field in required_fields:
            if field not in self.user_data:
                return False
        
        # Atualiza última validação
        self.user_data["last_validation"] = datetime.now().isoformat()
        self._save_license(self.user_data)
        
        return True
    
    def _validate_online(self) -> bool:
        """
        Validação online - verifica com servidor
        (Implementação opcional)
        """
        try:
            # Aqui você pode implementar validação com servidor
            # Por exemplo, verificar lista de tokens banidos
            # Ou validar contra API
            
            # Por enquanto, aceita qualquer token registrado
            return self._validate_offline()
            
        except Exception as e:
            # Em caso de erro, faz validação offline
            return self._validate_offline()
    
    def get_user_info(self) -> Optional[Dict]:
        """Retorna informações do usuário"""
        return self.user_data
    
    def is_registered(self) -> bool:
        """Verifica se usuário está registrado"""
        return self.user_data is not None
    
    def revoke_license(self):
        """Remove licença local"""
        if os.path.exists(self.license_path):
            os.remove(self.license_path)
        self.user_data = None
    
    def get_registration_stats(self) -> Dict:
        """Retorna estatísticas de uso"""
        if not self.user_data:
            return {}
        
        registered_date = datetime.fromisoformat(self.user_data.get("registered_at", ""))
        days_since_registration = (datetime.now() - registered_date).days
        
        return {
            "name": self.user_data.get("name"),
            "email": self.user_data.get("email"),
            "organization": self.user_data.get("organization", "Individual"),
            "registered_at": self.user_data.get("registered_at"),
            "days_active": days_since_registration,
            "version": self.user_data.get("version", "1.0.0")
        }


def require_license(func):
    """
    Decorator para funções que requerem licença válida
    """
    def wrapper(*args, **kwargs):
        license_manager = LicenseManager()
        
        if not license_manager.is_registered():
            print("\n" + "="*60)
            print("🔒 BackupMaster - Registro Necessário")
            print("="*60)
            print("\nO BackupMaster é GRATUITO, mas requer registro.")
            print("Isso nos ajuda a entender quem está usando o sistema.\n")
            
            # Solicita registro
            name = input("Nome: ").strip()
            email = input("Email: ").strip()
            organization = input("Organização (opcional): ").strip()
            
            if not name or not email:
                print("\n❌ Nome e email são obrigatórios!")
                return None
            
            result = license_manager.register_user(name, email, organization)
            
            print(f"\n✅ {result['message']}")
            print(f"🔑 Seu token: {result['token'][:20]}...")
            print("\nObrigado por usar o BackupMaster! 🎉\n")
        
        # Valida licença
        if not license_manager.validate_license(offline_mode=True):
            print("\n❌ Erro ao validar licença!")
            print("Por favor, registre-se novamente.\n")
            return None
        
        # Executa função
        return func(*args, **kwargs)
    
    return wrapper


def check_and_register():
    """
    Verifica e registra usuário se necessário
    Retorna True se registrado, False caso contrário
    """
    license_manager = LicenseManager()
    
    if license_manager.is_registered():
        # Valida licença existente
        if license_manager.validate_license(offline_mode=True):
            return True
        else:
            print("❌ Licença inválida. Por favor, registre-se novamente.")
            license_manager.revoke_license()
            return False
    
    return False


def show_license_info():
    """Mostra informações da licença"""
    license_manager = LicenseManager()
    
    if not license_manager.is_registered():
        print("\n❌ Nenhuma licença encontrada.")
        print("Execute o BackupMaster para se registrar.\n")
        return
    
    stats = license_manager.get_registration_stats()
    
    print("\n" + "="*60)
    print("🔑 Informações da Licença")
    print("="*60)
    print(f"\n👤 Nome: {stats.get('name')}")
    print(f"📧 Email: {stats.get('email')}")
    print(f"🏢 Organização: {stats.get('organization')}")
    print(f"📅 Registrado em: {stats.get('registered_at')}")
    print(f"⏱️  Dias de uso: {stats.get('days_active')}")
    print(f"📦 Versão: {stats.get('version')}")
    print("\n" + "="*60 + "\n")
