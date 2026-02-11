"""cached_models.py - Caching de modelos ML con @st.cache_resource"""

import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger

logger = get_logger(__name__)

@st.cache_resource
def get_transcriber():
    """Carga Transcriber UNA SOLA VEZ y lo cachea
    
    Returns:
        Instancia de Transcriber
    """
    try:
        from Transcriber import Transcriber
        logger.info("📦 Cargando Transcriber (se cacheará)")
        return Transcriber()
    except Exception as e:
        logger.error(f"Error al cargar Transcriber: {e}")
        raise

@st.cache_resource
def get_chat_model():
    """Carga Chat Model UNA SOLA VEZ y lo cachea
    
    Returns:
        Instancia de Model
    """
    try:
        from Model import Model
        logger.info("📦 Cargando Chat Model (se cacheará)")
        return Model()
    except Exception as e:
        logger.error(f"Error al cargar Model: {e}")
        raise

@st.cache_resource
def get_audio_recorder():
    """Carga AudioRecorder UNA SOLA VEZ y lo cachea
    
    Returns:
        Instancia de AudioRecorder
    """
    try:
        from AudioRecorder import AudioRecorder
        logger.info("📦 Cargando AudioRecorder (se cacheará)")
        return AudioRecorder()
    except Exception as e:
        logger.error(f"Error al cargar AudioRecorder: {e}")
        raise

@st.cache_resource
def get_opportunities_manager():
    """Carga OpportunitiesManager UNA SOLA VEZ y lo cachea
    
    Returns:
        Instancia de OpportunitiesManager
    """
    try:
        from OpportunitiesManager import OpportunitiesManager
        logger.info("📦 Cargando OpportunitiesManager (se cacheará)")
        return OpportunitiesManager()
    except Exception as e:
        logger.error(f"Error al cargar OpportunitiesManager: {e}")
        raise
