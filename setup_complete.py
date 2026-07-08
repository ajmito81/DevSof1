#!/usr/bin/env python3
"""
Script completo para setup do projeto PLC SKU Router
Cria toda a estrutura, arquivos e configura git
"""

import os
import subprocess
from pathlib import Path

class ProjectSetup:
    def __init__(self):
        self.base = Path.cwd()
    
    def create_folders(self):
        """Cria todas as pastas necessárias"""
        dirs = [
            'config', 'src', 'src/core', 'src/protocol', 'src/database',
            'src/services', 'src/api', 'src/workers', 'src/utils',
            'docs', 'tests', 'scripts', 'logs'
        ]
        
        for d in dirs:
            Path(d).mkdir(parents=True, exist_ok=True)
            init_file = Path(d) / '__init__.py'
            if not init_file.exists():
                init_file.touch()
        
        print("✅ Pastas criadas")
    
    def create_config_init(self):
        """Cria config/__init__.py"""
        content = '''from config.settings import settings

__all__ = ['settings']
'''
        (self.base / 'config' / '__init__.py').write_text(content)
        print("✅ config/__init__.py criado")
    
    def create_config_settings(self):
        """Cria config/settings.py"""
        content = '''# config/settings.py
"""
Configurações centralizadas do sistema.
Todas as configs de comunicação, banco, timeouts aqui.
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # ===== COMUNICAÇÃO PLC =====
    PLC_HOST: str = os.getenv("PLC_HOST", "192.168.25.110")
    PLC_PORT: int = int(os.getenv("PLC_PORT", "3005"))
    PLC_SOCKET_TIMEOUT: float = float(os.getenv("PLC_SOCKET_TIMEOUT", "5.0"))
    PLC_BUFFER_SIZE: int = int(os.getenv("PLC_BUFFER_SIZE", "4096"))
    PLC_RECONNECT_INTERVAL: float = float(os.getenv("PLC_RECONNECT_INTERVAL", "5.0"))
    PLC_KEEP_ALIVE_INTERVAL: int = int(os.getenv("PLC_KEEP_ALIVE_INTERVAL", "5"))
    
    # ===== TIMEOUTS (<20ms) =====
    LOOKUP_TIMEOUT_MS: float = float(os.getenv("LOOKUP_TIMEOUT_MS", "15.0"))
    RESPONSE_TIMEOUT_MS: float = float(os.getenv("RESPONSE_TIMEOUT_MS", "18.0"))
    TOTAL_TIMEOUT_MS: float = float(os.getenv("TOTAL_TIMEOUT_MS", "20.0"))
    RETRANSMIT_TIMEOUT_MS: float = float(os.getenv("RETRANSMIT_TIMEOUT_MS", "1000.0"))
    
    # ===== API AUXILIAR =====
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "3005"))
    API_WORKERS: int = int(os.getenv("API_WORKERS", "4"))
    
    # ===== BANCO DE DADOS =====
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "plc_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "secure_password")
    DB_NAME: str = os.getenv("DB_NAME", "sku_router_db")
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "3600"))
    
    # ===== CACHE EM MEMÓRIA =====
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_SIZE_MB: int = int(os.getenv("CACHE_SIZE_MB", "100"))
    
    # ===== LOGGING =====
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/plc_router.log")
    LOG_MAX_BYTES: int = int(os.getenv("LOG_MAX_BYTES", "10485760"))
    LOG_BACKUP_COUNT: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    
    # ===== PERFORMANCE =====
    CPU_CORE_PIN: Optional[int] = None if os.getenv("CPU_CORE_PIN") is None else int(os.getenv("CPU_CORE_PIN"))
    DISABLE_GC: bool = os.getenv("DISABLE_GC", "true").lower() == "true"
    THREAD_PRIORITY: str = os.getenv("THREAD_PRIORITY", "high")
    
    # ===== PROTOCOLO =====
    TELEGRAM_FIXED_LENGTH: int = 150
    HEADER_START_CHAR: str = "S"
    HEADER_START_CHAR2: str = "C"
    TLG_TYPE_DATA: int = 602
    TLG_TYPE_CONFIRMATION: int = 604
    TLG_TYPE_RESPONSE: int = 702
    TLG_TYPE_ALIVE: int = 3
    
    # ===== ALERTAS SLA =====
    SLA_WARNING_MS: float = float(os.getenv("SLA_WARNING_MS", "15.0"))
    SLA_CRITICAL_MS: float = float(os.getenv("SLA_CRITICAL_MS", "19.0"))
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

# Instância global
settings = Settings()
'''
        (self.base / 'config' / 'settings.py').write_text(content)
        print("✅ config/settings.py criado")
    
    def create_core_files(self):
        """Cria arquivos do core"""
        
        # core/enums.py
        enums_content = '''# src/core/enums.py
"""
Enums e constantes do sistema.
"""

from enum import IntEnum

class TelegramTypeEnum(IntEnum):
    """Tipos de telegrama"""
    ALIVE = 3
    DATA = 602
    CONFIRMATION = 604
    RESPONSE = 702

class DestinationEnum(IntEnum):
    """Destinos possíveis"""
    LINHA_A = 1
    LINHA_B = 2
    LINHA_C = 3
    QUALIDADE = 4
    REJEITO = 5
'''
        (self.base / 'src' / 'core' / 'enums.py').write_text(enums_content)
        print("✅ src/core/enums.py criado")
        
        # core/exceptions.py
        exceptions_content = '''# src/core/exceptions.py
"""
Exceções customizadas da aplicação.
"""

class ProtocolException(Exception):
    """Exceção base do protocolo"""
    pass

class InvalidTelegramException(ProtocolException):
    """Telegrama inválido"""
    pass

class SKUNotFoundException(Exception):
    """SKU não encontrado"""
    pass

class DatabaseException(Exception):
    """Erro de banco de dados"""
    pass

class CacheException(Exception):
    """Erro de cache"""
    pass

class PLCCommunicationException(Exception):
    """Erro de comunicação com PLC"""
    pass

class TimeoutException(Exception):
    """Timeout na operação"""
    pass

class ConfigurationException(Exception):
    """Erro de configuração"""
    pass
'''
        (self.base / 'src' / 'core' / 'exceptions.py').write_text(exceptions_content)
        print("✅ src/core/exceptions.py criado")
    
    def create_env_files(self):
        """Cria .env e .env.example"""
        env_content = '''# ===== COMUNICAÇÃO PLC =====
PLC_HOST=192.168.25.110
PLC_PORT=3005
PLC_SOCKET_TIMEOUT=5.0
PLC_BUFFER_SIZE=4096
PLC_RECONNECT_INTERVAL=5.0
PLC_KEEP_ALIVE_INTERVAL=5

# ===== TIMEOUTS (<20ms) =====
LOOKUP_TIMEOUT_MS=15.0
RESPONSE_TIMEOUT_MS=18.0
TOTAL_TIMEOUT_MS=20.0
RETRANSMIT_TIMEOUT_MS=1000.0

# ===== API AUXILIAR =====
API_HOST=127.0.0.1
API_PORT=3005
API_WORKERS=4

# ===== BANCO DE DADOS =====
DB_HOST=localhost
DB_PORT=5432
DB_USER=plc_user
DB_PASSWORD=secure_password
DB_NAME=sku_router_db
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10

# ===== CACHE =====
CACHE_ENABLED=true
CACHE_SIZE_MB=100

# ===== LOGGING =====
LOG_LEVEL=INFO
LOG_FILE=logs/plc_router.log

# ===== PERFORMANCE =====
CPU_CORE_PIN=2
DISABLE_GC=true
THREAD_PRIORITY=high

# ===== ALERTAS SLA =====
SLA_WARNING_MS=15.0
SLA_CRITICAL_MS=19.0
'''
        (self.base / '.env').write_text(env_content)
        (self.base / '.env.example').write_text(env_content)
        print("✅ .env e .env.example criados")
    
    def create_gitignore(self):
        """Cria .gitignore"""
        content = '''__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/
.vscode/
.idea/
*.swp
*.swo
*~
.env
.env.local
logs/
*.log
*.db
*.sqlite
*.sqlite3
.DS_Store
Thumbs.db
.pytest_cache/
.coverage
htmlcov/
'''
        (self.base / '.gitignore').write_text(content)
        print("✅ .gitignore criado")
    
    def create_requirements(self):
        """Cria requirements.txt"""
        content = '''# Database
psycopg2-binary==2.9.9
sqlalchemy==2.0.23

# API
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0

# Performance
uvloop==0.20.0

# Utilities
python-dotenv==1.0.0
psutil==6.0.0

# Development
pytest==7.4.3
black==23.12.1
flake8==6.1.0
'''
        (self.base / 'requirements.txt').write_text(content)
        print("✅ requirements.txt criado")
    
        