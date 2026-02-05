import json
import os
import streamlit as st
from datetime import datetime

RECORDINGS_FILE = "recordings.json"
OPPORTUNITIES_FILE = "opportunities.json"

def load_recordings():
    """Carga grabaciones del archivo JSON"""
    if os.path.exists(RECORDINGS_FILE):
        try:
            with open(RECORDINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_recording_to_db(filename: str, filepath: str, transcription: str = None):
    """Guarda grabación en JSON local"""
    try:
        recordings = load_recordings()
        
        new_recording = {
            "id": len(recordings) + 1,
            "filename": filename,
            "filepath": filepath,
            "transcription": transcription,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        recordings.append(new_recording)
        
        with open(RECORDINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(recordings, f, indent=2, ensure_ascii=False)
        
        st.success(f"✅ Grabado: {filename}")
        return new_recording["id"]
    except Exception as e:
        st.error(f"❌ Error guardando: {e}")
        return None

def get_all_recordings():
    """Obtiene todas las grabaciones"""
    return load_recordings()

def update_transcription(recording_id, transcription: str):
    """Actualiza la transcripción de una grabación"""
    try:
        recordings = load_recordings()
        for recording in recordings:
            if recording["id"] == recording_id:
                recording["transcription"] = transcription
                recording["updated_at"] = datetime.now().isoformat()
                break
        
        with open(RECORDINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(recordings, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error actualizando: {e}")
        return False

def load_opportunities():
    """Carga oportunidades del archivo JSON"""
    if os.path.exists(OPPORTUNITIES_FILE):
        try:
            with open(OPPORTUNITIES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_opportunity(recording_id, title: str, description: str):
    """Guarda una oportunidad en JSON local"""
    try:
        opportunities = load_opportunities()
        
        new_opportunity = {
            "id": len(opportunities) + 1,
            "recording_id": recording_id,
            "title": title,
            "description": description,
            "created_at": datetime.now().isoformat()
        }
        
        opportunities.append(new_opportunity)
        
        with open(OPPORTUNITIES_FILE, "w", encoding="utf-8") as f:
            json.dump(opportunities, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        st.error(f"Error guardando oportunidad: {e}")
        return False

def get_opportunities_by_recording(recording_id):
    """Obtiene las oportunidades de una grabación"""
    opportunities = load_opportunities()
    return [opp for opp in opportunities if opp["recording_id"] == recording_id]
