"""\nutilities.py - Utilidades comunes para la aplicación frontend
"""
from datetime import datetime
import hashlib
from typing import Tuple, Optional, Any
import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger
from frontend.notifications import show_success, show_error

logger = get_logger(__name__)


def process_audio_file(audio_bytes: bytes, filename: str, recorder: Any, db_utils: Any) -> Tuple[bool, Optional[str]]:
    """
    Procesa un archivo de audio (grabación o carga).
    
    Args:
        audio_bytes (bytes): Datos del audio
        filename (str): Nombre del archivo
        recorder: Instancia de AudioRecorder
        db_utils: Módulo de base de datos
        
    Returns:
        tuple: (éxito: bool, recording_id: str o None)
    """
    try:
        # Validar tamaño
        audio_size = len(audio_bytes) / (1024 * 1024)
        if audio_size > 100:
            show_error(f"Archivo demasiado grande ({audio_size:.1f}MB). Máximo: 100MB")
            logger.warning(f"Archivo rechazado por tamaño: {filename} ({audio_size:.1f}MB)")
            return False, None
        
        # Validar que no esté vacío
        if len(audio_bytes) == 0:
            show_error("El archivo de audio está vacío")
            return False, None
        
        # Calcular hash para deduplicación
        audio_hash = hashlib.md5(audio_bytes).hexdigest()
        
        # Verificar si ya fue procesado
        if audio_hash in st.session_state.processed_audios:
            logger.info(f"Audio ya procesado (hash: {audio_hash})")
            return False, None
        
        # Guardar localmente
        filepath = recorder.save_recording(audio_bytes, filename)
        
        # Guardar en Supabase
        recording_id = db_utils.save_recording_to_db(filename, filepath)
        
        # Marcar como procesado
        st.session_state.processed_audios.add(audio_hash)
        
        # Actualizar lista de grabaciones
        st.session_state.recordings = recorder.get_recordings_from_supabase()
        
        logger.info(f"Audio procesado exitosamente: {filename} (ID: {recording_id})")
        show_success(f"Audio '{filename}' guardado correctamente")
        
        return True, recording_id
        
    except ValueError as e:
        show_error(f"Validación falló: {str(e)}")
        logger.warning(f"Validación falló para {filename}: {e}")
        return False, None
    except Exception as e:
        show_error(f"Error al procesar audio: {str(e)}")
        logger.error(f"Error procesando audio {filename}: {e}")
        return False, None


def delete_audio(filename: str, recorder: Any, db_utils: Any) -> bool:
    """
    Elimina un archivo de audio de forma segura.
    
    Args:
        filename (str): Nombre del archivo a eliminar
        recorder: Instancia de AudioRecorder
        db_utils: Módulo de base de datos
        
    Returns:
        bool: True si se eliminó exitosamente
    """
    try:
        # Eliminar de Supabase
        db_utils.delete_recording_by_filename(filename)
        
        # Eliminar localmente
        recorder.delete_recording(filename)
        
        # Limpiar cache de procesados
        st.session_state.processed_audios.clear()
        
        # Actualizar localmente la lista sin hacer refetch a Supabase (más rápido)
        if filename in st.session_state.recordings:
            st.session_state.recordings.remove(filename)
        
        logger.info(f"Audio eliminado: {filename}")
        
        return True
        
    except Exception as e:
        show_error(f"Error al eliminar: {str(e)}")
        logger.error(f"Error eliminando {filename}: {e}")
        return False
