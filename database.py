import streamlit as st
from supabase import create_client, Client
import os
from datetime import datetime

@st.cache_resource
def init_supabase() -> Client:
    """Inicializa conexión con Supabase"""
    try:
        supabase_url = st.secrets.get("SUPABASE_URL")
        supabase_key = st.secrets.get("SUPABASE_KEY")
        
        # Debug: mostrar si existen los secrets
        if not supabase_url:
            return None
        if not supabase_key:
            return None
        
        # Limpiar espacios en blanco
        supabase_url = supabase_url.strip()
        supabase_key = supabase_key.strip()
        
        client = create_client(supabase_url, supabase_key)
        return client
    except Exception as e:
        return None

def save_recording_to_db(filename: str, filepath: str, transcription: str = None):
    """Guarda grabación en la base de datos"""
    try:
        db = init_supabase()
        if db is None:
            st.error("No se pudo conectar a Supabase")
            return False
        
        data = {
            "filename": filename,
            "filepath": filepath,
            "transcription": transcription,
            "created_at": datetime.now().isoformat()
        }
        
        response = db.table("recordings").insert(data).execute()
        
        if response.data:
            st.success(f"✅ Guardado en Supabase: {filename}")
            return response.data[0]["id"]
        else:
            st.warning(f"⚠️ No se guardó correctamente")
            return None
    except Exception as e:
        st.error(f"❌ Error guardando: {str(e)}")
        return None

def get_all_recordings():
    """Obtiene todas las grabaciones de la BD"""
    try:
        db = init_supabase()
        if db is None:
            return []
        
        response = db.table("recordings").select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error obteniendo grabaciones: {e}")
        return []

def update_transcription(recording_id: str, transcription: str):
    """Actualiza la transcripción de una grabación"""
    try:
        db = init_supabase()
        if db is None:
            return False
        
        response = db.table("recordings").update({
            "transcription": transcription,
            "updated_at": datetime.now().isoformat()
        }).eq("id", recording_id).execute()
        
        return True if response.data else False
    except Exception as e:
        st.error(f"Error actualizando transcripción: {e}")
        return False

def save_opportunity(recording_id: str, title: str, description: str):
    """Guarda una oportunidad asociada a una grabación"""
    try:
        db = init_supabase()
        if db is None:
            return False
        
        data = {
            "recording_id": recording_id,
            "title": title,
            "description": description,
            "created_at": datetime.now().isoformat()
        }
        
        response = db.table("opportunities").insert(data).execute()
        return True if response.data else False
    except Exception as e:
        st.error(f"Error guardando oportunidad: {e}")
        return False

def get_opportunities_by_recording(recording_id: str):
    """Obtiene las oportunidades de una grabación"""
    try:
        db = init_supabase()
        if db is None:
            return []
        
        response = db.table("opportunities").select("*").eq("recording_id", recording_id).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error obteniendo oportunidades: {e}")
        return []
