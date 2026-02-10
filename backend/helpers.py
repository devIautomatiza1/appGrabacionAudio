"""helpers.py - Funciones auxiliares comunes para reducir duplicación"""
import streamlit as st
from functools import wraps
from pathlib import Path
from typing import Callable, Optional, Any, Dict, List, Tuple
from datetime import datetime
from logger import get_logger

logger = get_logger(__name__)

def db_operation(func: Callable) -> Callable:
    """Decorador para operaciones BD: maneja conexión, excepciones y logging
    
    Automáticamente intenta obtener la conexión a BD y maneja errores comunes.
    Retorna None para funciones de lectura, False para escritura si falla.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            from database import init_supabase
            db = init_supabase()
            if not db: 
                logger.warning(f"{func.__name__}: BD no disponible")
                return None if func.__name__.endswith('_by_') or 'get' in func.__name__ else False
            return func(db, *args, **kwargs)
        except Exception as e:
            logger.error(f"{func.__name__}: {type(e).__name__} - {str(e)}")
            return None if 'get' in func.__name__ else False
    return wrapper

def validate_file(filepath: str, expected_ext: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """Valida que un archivo existe, es valid y tiene tamaño > 0
    
    Args:
        filepath: Ruta del archivo a validar
        expected_ext: Extensión esperada (opcional, ej: '.mp3')
        
    Returns:
        Tupla (válido: bool, mensaje_error: Optional[str])
    """
    p = Path(filepath)
    if not p.exists(): 
        return False, f"Archivo no encontrado: {filepath}"
    if not p.is_file(): 
        return False, f"No es un archivo: {filepath}"
    if p.stat().st_size == 0: 
        return False, f"Archivo vacío: {filepath}"
    if expected_ext and not str(filepath).lower().endswith(expected_ext):
        return False, f"Formato inválido. Esperado: {expected_ext}"
    return True, None

def table_query(db, table: str, method: str = "select", *args, **kwargs) -> Optional[List[Dict]]:
    """Helper para queries SQL simples en Supabase
    
    Args:
        db: Cliente de Supabase
        table: Nombre de la tabla
        method: Método a ejecutar ('select', 'insert', 'update', 'delete')
        *args, **kwargs: Argumentos para el método
        
    Returns:
        Lista de resultados o None si error
    """
    try:
        query = getattr(db.table(table), method)(*args, **kwargs)
        result = query.execute()
        return result.data if result and result.data else [] if method == "select" else result.data
    except Exception as e:
        logger.debug(f"Query {method} en {table}: {str(e)}")
        return [] if method == "select" else None

def log_operation(level: str = "info", prefix: str = "") -> Callable:
    """Decorador para logging automático de operaciones
    
    Registra entrada y salida de funciones automáticamente.
    
    Args:
        level: Nivel de log ('info', 'debug', 'warning')
        prefix: Prefijo para el mensaje de log
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                msg = f"{prefix}{func.__name__}: OK"
                getattr(logger, level)(msg if level == "info" else msg)
                return result
            except Exception as e:
                logger.error(f"{prefix}{func.__name__}: {type(e).__name__} - {str(e)}")
                raise
        return wrapper
    return decorator

def safe_json_dump(data: Dict, filename: str, dir_path: Path) -> bool:
    """Guarda datos en JSON de forma segura con validación y logging
    
    Args:
        data: Diccionario a guardar
        filename: Nombre del archivo
        dir_path: Ruta donde guardar
        
    Returns:
        True si éxito, False si error
    """
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        with open(dir_path / filename, "w", encoding="utf-8") as f:
            import json
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error guardando JSON: {str(e)}")
        return False

def format_recording_name(filename: str) -> str:
    """Limpia extensión de archivo y formatea el nombre para mostrar
    
    Args:
        filename: Nombre del archivo con extensión
        
    Returns:
        Nombre formateado sin extensión y con espacios en lugar de guiones
    """
    from config import AUDIO_EXTENSIONS
    
    # Quitar extensión
    for ext in AUDIO_EXTENSIONS:
        if filename.lower().endswith(f".{ext}"):
            filename = filename[:-len(ext)-1]
            break
    
    # Reemplazar guiones bajos por espacios
    return filename.replace("_", " ")
