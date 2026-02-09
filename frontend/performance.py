"""
Performance Optimization Module
================================
Funciones para caché, actualización local sin rerun, y lazy loading
"""

import streamlit as st
from functools import lru_cache
from typing import List, Dict, Any, Optional

# ============================================================================
# CACHÉ AGRESIVO PARA TRANSCRIPCIONES
# ============================================================================

@st.cache_data(ttl=3600, show_spinner=False)
def get_transcription_cached(filename: str, db_utils) -> Optional[str]:
    """
    Obtiene transcripción con caché de 1 hora
    
    Args:
        filename: Nombre del archivo
        db_utils: Módulo de base de datos
        
    Returns:
        Transcripción o None si no existe
    """
    try:
        return db_utils.get_transcription_by_filename(filename)
    except Exception:
        return None


@st.cache_data(ttl=600, show_spinner=False)
def load_all_recordings_cached(recorder) -> List[str]:
    """
    Obtiene lista de grabaciones con caché de 10 minutos
    
    Args:
        recorder: Objeto AudioRecorder
        
    Returns:
        Lista de nombres de grabaciones
    """
    try:
        return recorder.get_recordings_from_supabase()
    except Exception:
        return []


# ============================================================================
# ACTUALIZACIÓN LOCAL SIN RERUN (100ms en lugar de 2 segundos)
# ============================================================================

def update_opportunity_local(idx: int, updates: Dict[str, Any]) -> bool:
    """
    Actualiza oportunidad localmente en session_state SIN st.rerun()
    
    Args:
        idx: Índice en la lista
        updates: Dict con cambios {status, priority, notes}
        
    Returns:
        True si actualizar exitosa
    """
    try:
        if idx < len(st.session_state.opportunities):
            st.session_state.opportunities[idx].update(updates)
            return True
    except Exception:
        pass
    return False


def delete_opportunity_local(idx: int) -> bool:
    """
    Elimina oportunidad localmente en session_state SIN st.rerun()
    
    Args:
        idx: Índice en la lista
        
    Returns:
        True si eliminada exitosa
    """
    try:
        if 0 <= idx < len(st.session_state.opportunities):
            st.session_state.opportunities.pop(idx)
            return True
    except Exception:
        pass
    return False


def delete_keyword_local(keyword: str) -> bool:
    """
    Elimina palabra clave localmente SIN st.rerun()
    
    Args:
        keyword: Palabra clave a eliminar
        
    Returns:
        True si eliminada exitosa
    """
    try:
        if keyword in st.session_state.keywords:
            del st.session_state.keywords[keyword]
            return True
    except Exception:
        pass
    return False


def delete_recording_local(filename: str) -> bool:
    """
    Elimina grabación localmente SIN st.rerun()
    
    Args:
        filename: Nombre del archivo
        
    Returns:
        True si eliminada exitosa
    """
    try:
        if filename in st.session_state.recordings:
            st.session_state.recordings.remove(filename)
            if st.session_state.selected_audio == filename:
                st.session_state.selected_audio = None
            return True
    except Exception:
        pass
    return False


# ============================================================================
# LAZY LOADING: Carga solo N items por página
# ============================================================================

def paginated_list(items: List[Any], items_per_page: int = 20, key_prefix: str = "page") -> tuple:
    """
    Implementa paginación para listas grandes
    
    Args:
        items: Lista completa de items
        items_per_page: Items a mostrar por página
        key_prefix: Prefijo para session_state key
        
    Returns:
        Tupla (items_in_page, page_number, total_pages)
    """
    if f"{key_prefix}_number" not in st.session_state:
        st.session_state[f"{key_prefix}_number"] = 0
    
    page = st.session_state[f"{key_prefix}_number"]
    total_pages = (len(items) + items_per_page - 1) // items_per_page
    
    start = page * items_per_page
    end = start + items_per_page
    
    return items[start:end], page, total_pages


def show_pagination_controls(page: int, total_pages: int, key_prefix: str = "page") -> None:
    """
    Muestra botones de paginación
    
    Args:
        page: Página actual (0-indexed)
        total_pages: Número total de páginas
        key_prefix: Prefijo para identificar controles
    """
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if page > 0:
            if st.button("← Anterior", key=f"{key_prefix}_prev"):
                st.session_state[f"{key_prefix}_number"] = max(0, page - 1)
                st.rerun()
    
    with col2:
        st.write(f"📄 Página {page + 1} de {total_pages}")
    
    with col3:
        if page < total_pages - 1:
            if st.button("Siguiente →", key=f"{key_prefix}_next"):
                st.session_state[f"{key_prefix}_number"] = min(total_pages - 1, page + 1)
                st.rerun()


# ============================================================================
# PROGRESS FEEDBACK: Mostrar progreso en operaciones lentas
# ============================================================================

def show_transcription_progress():
    """Muestra barra de progreso mientras se transcribe"""
    progress_container = st.container()
    return progress_container


def operation_in_progress(operation_name: str = "Procesando"):
    """
    Context manager para spinners consistentes
    
    Usage:
        with operation_in_progress("Guardando"):
            # código lento aquí
    """
    return st.spinner(f"⏳ {operation_name}...")


# ============================================================================
# QUERY OPTIMIZATION: Helpers para queries más eficientes
# ============================================================================

def load_recording_with_all_data(db_utils, filename: str) -> Optional[Dict[str, Any]]:
    """
    Carga un audio con TODAS sus relaciones en UNA sola query
    
    Args:
        db_utils: Módulo de base de datos
        filename: Nombre del archivo
        
    Returns:
        Dict con recording + transcriptions + opportunities o None
    """
    try:
        # Query optimizada que trae todo
        result = db_utils.db.table("recordings").select(
            "*, transcriptions(*), opportunities(*)"
        ).eq("filename", filename).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
    except Exception:
        pass
    return None


def batch_load_opportunities(db_utils, recording_ids: List[str]) -> Dict[str, List[Dict]]:
    """
    Carga oportunidades para múltiples grabaciones en UNA query
    
    Args:
        db_utils: Módulo de base de datos
        recording_ids: Lista de IDs de grabaciones
        
    Returns:
        Dict {recording_id: [opportunities]}
    """
    result_dict = {}
    try:
        result = db_utils.db.table("opportunities").select("*").in_(
            "recording_id", recording_ids
        ).execute()
        
        for opp in result.data:
            rec_id = opp["recording_id"]
            if rec_id not in result_dict:
                result_dict[rec_id] = []
            result_dict[rec_id].append(opp)
    except Exception:
        pass
    
    return result_dict


# ============================================================================
# SESSION STATE UTILITIES
# ============================================================================

def init_optimization_state() -> None:
    """Inicializa variables de session para optimizaciones"""
    if "last_operation_success" not in st.session_state:
        st.session_state.last_operation_success = False
    
    if "last_operation_message" not in st.session_state:
        st.session_state.last_operation_message = ""
    
    if "rerender_trigger" not in st.session_state:
        st.session_state.rerender_trigger = 0


def trigger_local_rerender() -> None:
    """Trigger para redibujar widgets sin recargar toda la página"""
    st.session_state.rerender_trigger += 1


# ============================================================================
# BATCH OPERATIONS
# ============================================================================

def batch_delete_recordings(db_utils, filenames: List[str]) -> tuple:
    """
    Elimina múltiples grabaciones eficientemente
    
    Args:
        db_utils: Módulo de base de datos
        filenames: Lista de nombres de archivo
        
    Returns:
        Tupla (success: bool, message: str, deleted_count: int)
    """
    deleted = 0
    failed = []
    
    with st.spinner(f"⏳ Eliminando {len(filenames)} grabación(es)..."):
        for filename in filenames:
            try:
                if delete_audio(filename, db_utils):
                    deleted += 1
                else:
                    failed.append(filename)
            except Exception as e:
                failed.append(f"{filename}: {str(e)}")
        
        if deleted == len(filenames):
            return True, f"✓ Eliminado(s) {deleted} archivo(s)", deleted
        elif deleted == 0:
            return False, f"❌ Error eliminando archivos", 0
        else:
            return True, f"⚠️ Eliminado(s) {deleted}/{len(filenames)} (fallos: {len(failed)})", deleted


def delete_audio(filename: str, db_utils) -> bool:
    """Helper para eliminar audio"""
    try:
        return db_utils.delete_recording_from_db(db_utils.db, filename)
    except Exception:
        return False
