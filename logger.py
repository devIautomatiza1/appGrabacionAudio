"""
logger.py - Logging centralizado con múltiples handlers
"""
import logging
import sys
from pathlib import Path

# Importar config (evitar circular imports)
try:
    from config import LOG_LEVEL, LOG_FILE
except ImportError:
    LOG_LEVEL = "INFO"
    LOG_FILE = Path("./data/app.log")

# ============================================================================
# CONFIGURACIÓN DEL LOGGER
# ============================================================================

logger = logging.getLogger("app_audio")
logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

# Evitar múltiples handlers si se importa varias veces
if not logger.handlers:
    # Formato detallado para logs
    detailed_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola (con colores en stderr)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(detailed_format)
    logger.addHandler(console_handler)
    
    # Handler para archivo (con logs más detallados)
    try:
        # Crear directorio si no existe
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_format)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"No se pudo crear archivo de logs: {e}")

def get_logger(name: str) -> logging.Logger:
    """Obtiene un logger hijo con el nombre especificado
    
    Args:
        name: Nombre del módulo (típicamente __name__)
        
    Returns:
        Logger configurado para el módulo
    """
    return logging.getLogger(f"app_audio.{name}")

