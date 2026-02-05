"""
Configuración centralizada del aplicativo
Carga variables de entorno y valida configuración
"""

import os
import sys
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

class Settings:
    """Configuración de la aplicación"""
    
    # Aplicación
    APP_NAME: str = "iPrevencion API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Base de Datos
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/iprevencion"
    )
    
    # JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Gemini API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
    ALLOWED_AUDIO_FORMATS: list = ["mp3", "wav", "m4a", "flac", "webm", "ogg"]
    
    # CORS
    ALLOWED_ORIGINS: str = os.getenv(
        "ALLOWED_ORIGINS", 
        "http://localhost:3000,http://localhost:8501"
    )
    
    # Railway Environment Variables
    RAILWAY_PRIVATE_DOMAIN: str = os.getenv("RAILWAY_PRIVATE_DOMAIN", "")
    RAILWAY_SERVICE_NAME: str = os.getenv("RAILWAY_SERVICE_NAME", "")
    RAILWAY_ENVIRONMENT_NAME: str = os.getenv("RAILWAY_ENVIRONMENT_NAME", "")
    
    def validate(self):
        """Valida configuración crítica"""
        # En producción, SECRET_KEY no debe ser default
        if self.ENVIRONMENT == "production" and self.SECRET_KEY == "your-secret-key-change-in-production":
            raise ValueError(
                "🚨 SECURITY ERROR: SECRET_KEY es default en producción!\\n"
                "Genera new con: python -c \\\"import secrets; print(secrets.token_urlsafe(32))\\\""
            )
        
        # GEMINI_API_KEY es obligatorio
        if not self.GEMINI_API_KEY:
            raise ValueError(
                "🚨 ERROR: GEMINI_API_KEY no configurada!\\n"
                "Obtén gratis en: https://makersuite.google.com/app/apikey"
            )
        
        # DATABASE_URL debe ser válida
        if not self.DATABASE_URL or self.DATABASE_URL == "postgresql://user:password@localhost:5432/iprevencion":
            if self.ENVIRONMENT == "production":
                raise ValueError(
                    "🚨 ERROR: DATABASE_URL inválida en producción!\\n"
                    "Usa la URL de Railway con: postgresql://postgres@appgrabacionaudio.railway.internal:5432/iprevencion"
                )
        
        print(f"✅ Configuración validada - Ambiente: {self.ENVIRONMENT}")
    
    # Seguridad
    PASSWORD_MIN_LENGTH: int = 8
    ENABLE_AUDIT_LOG: bool = os.getenv("ENABLE_AUDIT_LOG", "true").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Obtiene la instancia de configuración (cached)"""
    return Settings()
