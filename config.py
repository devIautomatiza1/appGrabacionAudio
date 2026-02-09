"""
config.py - Configuración centralizada de la aplicación
"""
from pathlib import Path
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Rutas base
APP_ROOT = Path(__file__).parent
DATA_DIR = APP_ROOT / "data"
RECORDINGS_DIR = DATA_DIR / "recordings"
OPPORTUNITIES_DIR = DATA_DIR / "opportunities"

# Crear directorios si no existen
RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
OPPORTUNITIES_DIR.mkdir(parents=True, exist_ok=True)

# Configuración de audio
AUDIO_EXTENSIONS = ("mp3", "wav", "m4a", "ogg", "flac", "webm")
MAX_AUDIO_SIZE_MB = 100  # Tamaño máximo de archivo en MB
MIME_TYPES = {
    'mp3': 'audio/mpeg',
    'wav': 'audio/wav',
    'm4a': 'audio/mp4',
    'flac': 'audio/flac',
    'webm': 'audio/webm',
    'ogg': 'audio/ogg',
}

# Configuración de Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY no está configurada en el archivo .env")

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validar credenciales críticas
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Error de configuración: Faltan credenciales de Supabase.\n"
        "Asegúrate de que .env contiene:\n"
        "  - SUPABASE_URL\n"
        "  - SUPABASE_KEY\n"
        "Para Streamlit Cloud, configúralas en Settings > Secrets"
    )

# Configuración de la aplicación
APP_NAME = "Sistema Control Reuniones"
APP_DESCRIPTION = "Sistema inteligente de análisis de audios con IA para gestión de oportunidades"
APP_VERSION = "1.0.0"

# Modelos de IA
TRANSCRIPTION_MODEL = "gemini-2.0-flash"
CHAT_MODEL = "gemini-2.0-flash"

# Opciones de estado y prioridad
STATUS_OPTIONS = ["new", "in_progress", "closed", "won"]
PRIORITY_OPTIONS = ["Low", "Medium", "High"]

# Configuración de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = DATA_DIR / "app.log"
