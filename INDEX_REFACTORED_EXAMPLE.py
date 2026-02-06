# 📝 EJEMPLO: index.py Refactorizado
# Este archivo muestra cómo debería lucir el código después de refactorizar
# Úsalo como referencia para actualizar tu index.py existente

import streamlit as st
import os
from datetime import datetime
from pathlib import Path

# ✅ IMPORTS REFACTORIZADOS - Backend (servicios, no BD directa)
from backend.services import AudioService, TranscriptionService, OpportunityService
from ui.styles import get_styles
from ui.notifications import (
    show_success, show_error, show_warning, show_info,
    show_success_expanded, show_error_expanded, show_info_expanded
)

# Módulos de utilidad (sin cambios)
import AudioRecorder
import Transcriber
import Model
import OpportunitiesManager

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

st.set_page_config(layout="wide", page_title="Sistema Control Audio Iprevencion")
st.markdown(get_styles(), unsafe_allow_html=True)

# ============================================================================
# INICIALIZACIÓN DE SERVICIOS (Nuevo patrón)
# ============================================================================

# Las tres capas de servicios disponibles
audio_service = AudioService()
trans_service = TranscriptionService()
opp_service = OpportunityService()

# Módulos de utilidad (mantener por compatibilidad)
recorder = AudioRecorder.AudioRecorder()
transcriber_model = Transcriber.Transcriber()
chat_model = Model.Model()
opp_manager = OpportunitiesManager.OpportunitiesManager()

# ============================================================================
# ESTADO DE SESIÓN
# ============================================================================

if "processed_audios" not in st.session_state:
    st.session_state.processed_audios = set()

# ✅ Usar servicio para obtener grabaciones (en lugar de dirección directa a Supabase)
if "recordings" not in st.session_state:
    st.session_state.recordings = audio_service.get_all_recordings()

if "is_deleting" not in st.session_state:
    st.session_state.is_deleting = False

if "selected_audio" not in st.session_state:
    st.session_state.selected_audio = None

if "keywords" not in st.session_state:
    st.session_state.keywords = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ============================================================================
# SECCIÓN 1: GRABADORA EN VIVO
# ============================================================================

st.title("Sistema Control Audio Iprevencion")
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<h3 style="color: white;">Grabadora en vivo</h3>', unsafe_allow_html=True)
    st.caption("Graba directamente desde tu micrófono")
    
    audio_data = st.audio_input("Presiona para grabar:", key="audio_recorder")
    
    if audio_data:
        # ✅ Guardar localmente
        filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        filepath = f"recordings/{filename}"
        Path("recordings").mkdir(exist_ok=True)
        
        with open(filepath, "wb") as f:
            f.write(audio_data.getbuffer())
        
        # ✅ Guardar en BD vía servicio (NO directamente a Supabase)
        recording_id = audio_service.save_recording(filename, filepath)
        
        if recording_id:
            show_success(f"Grabación guardada: {filename}")
            st.session_state.recordings = audio_service.get_all_recordings()
            st.rerun()
        else:
            show_error("Error al guardar la grabación")

# ============================================================================
# SECCIÓN 2: CARGA DE ARCHIVO
# ============================================================================

with col2:
    st.markdown('<h3 style="color: white;">Cargar archivo</h3>', unsafe_allow_html=True)
    st.caption("Sube un archivo de audio")
    
    uploaded_file = st.file_uploader("Selecciona un archivo", type=["wav", "mp3", "m4a"])
    
    if uploaded_file:
        filename = uploaded_file.name
        filepath = f"recordings/{filename}"
        Path("recordings").mkdir(exist_ok=True)
        
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # ✅ Guardar en BD vía servicio
        recording_id = audio_service.save_recording(filename, filepath)
        
        if recording_id:
            show_success(f"Archivo cargado: {filename}")
            st.session_state.recordings = audio_service.get_all_recordings()
            st.rerun()
        else:
            show_error("Error al cargar archivo")

# ============================================================================
# SECCIÓN 3: LISTA DE AUDIOS
# ============================================================================

st.markdown("---")
st.markdown('<h3 style="color: white;">Audios Grabados</h3>', unsafe_allow_html=True)

if st.session_state.recordings:
    # Convert BD records to list of filenames for dropdown
    filenames = [rec.get("filename") if isinstance(rec, dict) else rec for rec in st.session_state.recordings]
    
    selected = st.selectbox("Selecciona un audio:", filenames)
    
    if selected:
        st.session_state.selected_audio = selected
        
        # ✅ Obtener datos del recording desde BD vía servicio
        recording = audio_service.get_recording_by_filename(selected)
        
        if recording:
            st.write(f"**Grabado**: {recording.get('created_at', 'N/A')}")
            
            # Reproducir si existe archivo
            filepath = f"recordings/{selected}"
            if os.path.exists(filepath):
                st.audio(filepath)
            
            # ✅ TRANSCRIBIR
            if st.button("Transcribir audio"):
                with st.spinner("Transcribiendo..."):
                    try:
                        transcription = transcriber_model.transcript_audio(filepath)
                        
                        # ✅ Guardar transcripción vía servicio
                        trans_id = trans_service.save_transcription(
                            recording_id=recording["id"],
                            content=transcription,
                            language="es"
                        )
                        
                        if trans_id:
                            show_success("Transcripción guardada")
                            st.session_state.contexto = transcription
                            st.rerun()
                        else:
                            show_error("Error guardando transcripción")
                    
                    except Exception as e:
                        show_error(f"Error transcribiendo: {str(e)}")
            
            # ✅ EXTRAER PALABRAS CLAVE
            keywords_input = st.text_input("Palabras clave (separadas por coma):")
            if keywords_input:
                keywords = {kw.strip(): {} for kw in keywords_input.split(",")}
                st.session_state.keywords = keywords
            
            if st.session_state.keywords and st.session_state.get("contexto"):
                if st.button("Generar Ticket de Análisis"):
                    with st.spinner("Analizando..."):
                        # ✅ Usar servicio para extraer oportunidades automáticamente
                        created_ids = opp_service.extract_opportunities_from_keywords(
                            recording_id=recording["id"],
                            transcription=st.session_state.contexto,
                            keywords=st.session_state.keywords
                        )
                        
                        if created_ids:
                            show_success(f"{len(created_ids)} oportunidades identificadas")
                        else:
                            show_warning("No se identificaron oportunidades")
            
            # ✅ ELIMINAR GRABACIÓN (cascada)
            if st.button("Eliminar grabación"):
                if audio_service.delete_recording(recording["id"]):
                    show_success("Grabación eliminada")
                    st.session_state.recordings = audio_service.get_all_recordings()
                    st.rerun()
                else:
                    show_error("Error al eliminar")
else:
    show_info("No hay grabaciones yet")

# ============================================================================
# SECCIÓN 4: OPORTUNIDADES
# ============================================================================

st.markdown("---")
st.markdown('<h3 style="color: white;">Oportunidades Identificadas</h3>', unsafe_allow_html=True)

if st.session_state.selected_audio:
    recording = audio_service.get_recording_by_filename(st.session_state.selected_audio)
    
    if recording:
        # ✅ Obtener oportunidades vía servicio
        opportunities = opp_service.get_opportunities_by_recording(recording["id"])
        
        if opportunities:
            for opp in opportunities:
                with st.expander(f"📍 {opp.get('title', 'Oportunidad')}"):
                    st.write(f"**Descripción**: {opp.get('description', 'N/A')}")
                    st.write(f"**Creada**: {opp.get('created_at', 'N/A')}")
        else:
            show_info("Genera un análisis para ver oportunidades")
else:
    show_info("Selecciona un audio para ver oportunidades")

# ============================================================================
# SECCIÓN 5: CHAT CON IA
# ============================================================================

st.markdown("---")
st.markdown('<h3 style="color: white;">Asistente IA para Análisis de Reuniones</h3>', unsafe_allow_html=True)

if st.session_state.get("keywords"):
    show_info(f"Palabras clave activas: {', '.join(st.session_state.keywords.keys())}")

if st.session_state.chat_history:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state.chat_history:
        if message.startswith("👤"):
            user_text = message.replace("👤 **Usuario**: ", "")
            st.markdown(f'''
            <div class="chat-message chat-message-user">
                <div class="chat-avatar chat-avatar-user avatar-pulse">👤</div>
                <div class="chat-bubble chat-bubble-user">{user_text}</div>
            </div>
            ''', unsafe_allow_html=True)
        elif message.startswith("🤖"):
            ai_text = message.replace("🤖 **IA**: ", "")
            st.markdown(f'''
            <div class="chat-message chat-message-ai">
                <div class="chat-avatar chat-avatar-ai avatar-spin">✨</div>
                <div class="chat-bubble chat-bubble-ai">{ai_text}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

col_left, col_input, col_right = st.columns([1, 3, 1])
with col_input:
    user_input = st.chat_input("Escribe tu pregunta o solicitud de análisis...")

if user_input:
    st.session_state.chat_history.append(f"👤 **Usuario**: {user_input}")
    
    with st.spinner("Generando respuesta..."):
        try:
            keywords = st.session_state.get("keywords", {})
            context = st.session_state.get("contexto", "")
            response = chat_model.call_model(user_input, context, keywords)
            st.session_state.chat_history.append(f"🤖 **IA**: {response}")
            st.rerun()
        except Exception as e:
            show_error(f"Error al generar respuesta: {e}")

# ============================================================================
# SECCIÓN 6: DEBUG (Solo en desarrollo)
# ============================================================================

if st.checkbox("Ver debug info"):
    st.markdown("---")
    st.markdown("**Debug Info**")
    
    if st.session_state.recordings:
        show_info_expanded(f"Total grabaciones: {len(st.session_state.recordings)}")
    
    if st.session_state.selected_audio:
        recording = audio_service.get_recording_by_filename(st.session_state.selected_audio)
        if recording:
            show_info_expanded(f"Recording ID: {recording.get('id')}")
            show_info_expanded(f"Archivo: {recording.get('filename')}")
    
    if st.session_state.keywords:
        show_info_expanded(f"Palabras clave: {list(st.session_state.keywords.keys())}")

# ============================================================================
# NOTAS IMPORTANTES
# ============================================================================
"""
✅ CAMBIOS CLAVE EN ESTA REFACTORIZACIÓN:

1. SERVICIOS EN LUGAR DE BD DIRECTA:
   - audio_service.save_recording() en lugar de db_utils.save_recording_to_db()
   - audio_service.get_all_recordings() en lugar de dirección directa
   - trans_service.save_transcription() en lugar de db_utils.save_transcription()
   - opp_service.create_opportunity() o extract_opportunities_from_keywords()
   - audio_service.delete_recording() que automáticamente elimina dependencias

2. SEGURIDAD:
   - Credenciales en .env (nunca en código)
   - Validaciones en backend (antes de persistir)
   - Cliente Supabase único (singleton)

3. ESTRUCTURA:
   - Frontend (index.py) - Solo UI y lógica de presentación
   - Backend (backend/) - Todo lo demás
   - UI (ui/) - Componentes compartidos (estilos, notificaciones)

4. NOTIFICACIONES:
   - show_success(), show_error(), show_warning(), show_info()
   - No usar st.success(), st.error(), etc. directamente

CONVERSIÓN MANUAL:
Para cada lugar donde usabas database.py, reemplaza con el servicio 
correspondiente. La guía MIGRATION_GUIDE.md tiene ejemplos específicos.
"""
