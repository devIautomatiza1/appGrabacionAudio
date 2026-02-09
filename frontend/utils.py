"""utils.py - Utilidades comunes (~75 líneas)"""
import hashlib
import streamlit as st
from pathlib import Path
from typing import Tuple, Optional, Any
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger
from frontend.notifications import show_success, show_error

logger = get_logger(__name__)

def process_audio_file(audio_bytes: bytes, filename: str, recorder: Any, db_utils: Any) -> Tuple[bool, Optional[str]]:
    """Procesa un archivo de audio (grabación o carga)"""
    try:
        if len(audio_bytes) / (1024 * 1024) > 100:
            show_error("Archivo > 100MB")
            return False, None
        
        if not audio_bytes:
            show_error("Audio vacío")
            return False, None
        
        audio_hash = hashlib.md5(audio_bytes).hexdigest()
        if audio_hash in st.session_state.processed_audios:
            logger.info(f"Audio ya procesado: {audio_hash}")
            return False, None
        
        filepath = recorder.save_recording(audio_bytes, filename)
        recording_id = db_utils.save_recording_to_db(filename, filepath)
        
        if not recording_id:
            show_error("Error: No se guardó en Supabase")
            logger.error(f"BD falló: {filename}")
            return False, None
        
        st.session_state.processed_audios.add(audio_hash)
        st.session_state.recordings = recorder.get_recordings_from_supabase()
        
        logger.info(f"✓ Audio OK: {filename} (ID: {recording_id})")
        show_success(f"'{filename}' guardado en Supabase")
        return True, recording_id
    
    except (ValueError, FileNotFoundError) as e:
        show_error(f"Error: {str(e)}")
        logger.warning(f"Validación falló: {filename} - {e}")
        return False, None
    
    except Exception as e:
        show_error(f"Error procesando: {str(e)}")
        logger.error(f"Error: {filename} - {e}")
        return False, None

def delete_audio(filename: str, recorder: Any, db_utils: Any) -> bool:
    """Elimina un archivo de audio"""
    try:
        db_utils.delete_recording_by_filename(filename)
        recorder.delete_recording(filename)
        st.session_state.processed_audios.clear()
        
        if filename in st.session_state.recordings:
            st.session_state.recordings.remove(filename)
        
        logger.info(f"✓ Eliminado: {filename}")
        return True
    
    except Exception as e:
        show_error(f"Error al eliminar: {str(e)}")
        logger.error(f"Delete error: {filename} - {e}")
        return False
