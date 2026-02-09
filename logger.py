"""
logger.py - Logging centralizado para la aplicación
"""
import logging
import sys
from config import LOG_LEVEL, LOG_FILE

# Crear logger principal
logger = logging.getLogger("app_audio")
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

# Formato de logs
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Handler para consola
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

# Handler para archivo
try:
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
except Exception as e:
    logger.warning(f"No se pudo crear archivo de logs: {e}")

def get_logger(name):
    """Obtiene un logger con el nombre especificado"""
    return logging.getLogger(f"app_audio.{name}")
