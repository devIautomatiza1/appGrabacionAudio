import streamlit as st
import os
from datetime import datetime
import hashlib
import styles
from notifications import show_success, show_error, show_warning, show_info, show_success_expanded, show_error_expanded, show_info_expanded
from Model import Model
from backend.services.audio_service import AudioService
from backend.services.transcription_service import TranscriptionService
from backend.services.opportunity_service import OpportunityService
from backend.config import Config
from backend.supabase_client import get_supabase_client

# Configuración inicial de la interfaz de usuario
st.set_page_config(layout="wide", page_title="Sistema Control Audio Iprevencion")

# Cargar estilos CSS desde archivo
st.markdown(styles.get_styles(), unsafe_allow_html=True)

# ====== DEBUG: Verificar credenciales al cargar la app ======
if not st.session_state.get("_debug_shown", False):
    st.write("[DEBUG] Verificando configuración...")
    print("[DEBUG] ===== VERIFICACIÓN DE CONFIGURACIÓN =====")
    print(f"[DEBUG] SUPABASE_URL: {Config.get_supabase_url()[:30] if Config.get_supabase_url() else 'VACIO'}...")
    print(f"[DEBUG] SUPABASE_KEY: {Config.get_supabase_key()[:30] if Config.get_supabase_key() else 'VACIO'}...")
    print(f"[DEBUG] GEMINI_API_KEY: {'OK' if Config.get_gemini_api_key() else 'VACIO'}...")
    
    supabase = get_supabase_client()
    print(f"[DEBUG] Conexion Supabase: {'[OK] CONECTADO' if supabase else '[FALLO] NO CONECTADO'}")
    
    if supabase:
        st.write("[OK] Conexion a Supabase verificada")
    else:
        st.error("[ERROR] No hay conexion a Supabase. Verifica los secrets en Streamlit Cloud o credenciales en .env")
    
    st.session_state._debug_shown = True
    print("[DEBUG] ===== FIN VERIFICACION =====\n")

# Inicializar servicios del backend
audio_service = AudioService()
transcription_service = TranscriptionService()
opportunity_service = OpportunityService()
chat_model = Model()

# Inicializar estado de sesión
if "processed_audios" not in st.session_state:
    st.session_state.processed_audios = set()
if "recordings" not in st.session_state:
    st.session_state.recordings = audio_service.get_all_recordings()
if "is_deleting" not in st.session_state:
    st.session_state.is_deleting = False
if "selected_audio" not in st.session_state:
    st.session_state.selected_audio = None
if "upload_key_counter" not in st.session_state:
    st.session_state.upload_key_counter = 0
if "record_key_counter" not in st.session_state:
    st.session_state.record_key_counter = 0
if "chat_enabled" not in st.session_state:
    st.session_state.chat_enabled = False
if "contexto" not in st.session_state:
    st.session_state.contexto = ""
if "keywords" not in st.session_state:
    st.session_state.keywords = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Sistema Control Audio Iprevencion")

# Crear dos columnas principales para la carga
col1, col2 = st.columns([1, 1])

with col1:
    # GRABADORA DE AUDIO EN VIVO
    st.markdown('<h3 style="color: white;">Grabadora en vivo</h3>', unsafe_allow_html=True)
    st.caption("Graba directamente desde tu micrófono (sin interrupciones)")
    
    audio_data = st.audio_input("Presiona el botón para grabar:", key=f"audio_recorder_{st.session_state.record_key_counter}")
    
    # Procesar audio grabado SOLO UNA VEZ por hash
    if audio_data is not None:
        audio_bytes = audio_data.getvalue()
        if len(audio_bytes) > 0:
            audio_hash = hashlib.md5(audio_bytes).hexdigest()
            
            if audio_hash not in st.session_state.processed_audios:
                try:
                    os.makedirs("recordings", exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"recording_{timestamp}.wav"
                    audio_path = f"recordings/{filename}"
                    
                    with open(audio_path, "wb") as f:
                        f.write(audio_bytes)
                    
                    # Guardar referencia en BD
                    recording_id = audio_service.save_recording(filename, audio_path)
                    
                    st.session_state.processed_audios.add(audio_hash)
                    st.session_state.recordings = audio_service.get_all_recordings()
                    
                    show_success(f"Audio '{filename}' grabado y guardado")
                    st.session_state.record_key_counter += 1
                    
                except Exception as e:
                    show_error(f"Error al grabar: {str(e)}")
    
    # Opción de subir archivo
    st.markdown('<h3 style="color: white;">Sube un archivo de audio</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Selecciona un archivo de audio", type=["mp3", "wav", "m4a", "ogg", "flac", "webm"], key=f"audio_uploader_{st.session_state.upload_key_counter}")
    
    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        if len(audio_bytes) > 0:
            audio_hash = hashlib.md5(audio_bytes).hexdigest()
            
            if audio_hash not in st.session_state.processed_audios:
                try:
                    os.makedirs("recordings", exist_ok=True)
                    filename = uploaded_file.name
                    audio_path = f"recordings/{filename}"
                    
                    with open(audio_path, "wb") as f:
                        f.write(audio_bytes)
                    
                    recording_id = audio_service.save_recording(filename, audio_path)
                    
                    st.session_state.processed_audios.add(audio_hash)
                    st.session_state.recordings = audio_service.get_all_recordings()
                    
                    show_success(f"Archivo '{filename}' cargado y guardado")
                    st.session_state.upload_key_counter += 1
                    
                except Exception as e:
                    show_error(f"Error al cargar: {str(e)}")

with col2:
    st.markdown('<h3 style="color: white;">Audios Guardados</h3>', unsafe_allow_html=True)
    
    recordings = audio_service.get_all_recordings()
    st.session_state.recordings = recordings
    
    if recordings:
        # Extraer filenames de los dicts
        recording_filenames = [r.get('filename', '') for r in recordings if r.get('filename')]
        
        show_info(f"Total: {len(recording_filenames)} audio(s)")
        
        tab1, tab2 = st.tabs(["Transcribir", "Gestión en lote"])
        
        with tab1:
            if recording_filenames:
                selected_audio = st.selectbox(
                    "Selecciona un audio para transcribir",
                    recording_filenames,
                    format_func=lambda x: x.replace("_", " ").replace(".wav", "").replace(".mp3", "").replace(".m4a", "").replace(".webm", "").replace(".ogg", "").replace(".flac", "")
                )
                
                if selected_audio:
                    if selected_audio != st.session_state.get("loaded_audio"):
                        existing_transcription = transcription_service.get_by_filename(selected_audio)
                        if existing_transcription:
                            st.session_state.contexto = existing_transcription.get("content", "")
                            st.session_state.selected_audio = selected_audio
                            st.session_state.loaded_audio = selected_audio
                            st.session_state.chat_enabled = True
                            st.session_state.keywords = {}
                            show_info("Transcripción cargada desde BD")
                    
                    col_play, col_transcribe, col_delete = st.columns([1, 1, 1])
                    
                    with col_play:
                        if st.button("Reproducir"):
                            audio_path = f"recordings/{selected_audio}"
                            if os.path.exists(audio_path):
                                with open(audio_path, "rb") as f:
                                    st.audio(f.read(), format=f"audio/{selected_audio.split('.')[-1]}")
                    
                    with col_transcribe:
                        if st.button("Transcribir"):
                            with st.spinner("Transcribiendo..."):
                                try:
                                    audio_path = f"recordings/{selected_audio}"
                                    transcription = transcription_service.transcribe(audio_path)
                                    
                                    st.session_state.contexto = transcription
                                    st.session_state.selected_audio = selected_audio
                                    st.session_state.loaded_audio = selected_audio
                                    st.session_state.chat_enabled = True
                                    st.session_state.keywords = {}
                                    
                                    transcription_service.save(selected_audio, transcription)
                                    show_success("Transcripción completada y guardada")
                                except Exception as e:
                                    show_error(f"Error al transcribir: {e}")
                    
                    with col_delete:
                        if st.button("Eliminar", key=f"delete_{selected_audio}"):
                            try:
                                audio_service.delete_recording_by_filename(selected_audio)
                                if os.path.exists(f"recordings/{selected_audio}"):
                                    os.remove(f"recordings/{selected_audio}")
                                
                                st.session_state.processed_audios.clear()
                                st.session_state.recordings = audio_service.get_all_recordings()
                                st.session_state.chat_enabled = False
                                st.session_state.loaded_audio = None
                                show_success("Audio eliminado correctamente")
                                st.rerun()
                            except Exception as e:
                                show_error(f"Error al eliminar: {str(e)}")
        
        with tab2:
            st.subheader("Eliminar múltiples audios")
            st.write("Selecciona uno o varios audios para eliminarlos")
            
            if recording_filenames:
                audios_to_delete = st.multiselect(
                    "Audios a eliminar:",
                    recording_filenames,
                    format_func=lambda x: x.replace("_", " ").replace(".wav", "").replace(".mp3", "").replace(".m4a", "").replace(".webm", "").replace(".ogg", "").replace(".flac", "")
                )
                
                if audios_to_delete:
                    show_warning(f"Vas a eliminar {len(audios_to_delete)} audio(s)")
                    
                    st.write("**Audios seleccionados:**")
                    for audio in audios_to_delete:
                        st.write(f"  • {audio}")
                    
                    col_confirm, col_cancel = st.columns(2)
                    with col_confirm:
                        if st.button("Eliminar seleccionados", type="primary", use_container_width=True, key="delete_batch"):
                            deleted_count = 0
                            
                            try:
                                for audio in audios_to_delete:
                                    try:
                                        audio_service.delete_recording_by_filename(audio)
                                        if os.path.exists(f"recordings/{audio}"):
                                            os.remove(f"recordings/{audio}")
                                        deleted_count += 1
                                    except Exception as e:
                                        show_error(f"Error al eliminar {audio}: {e}")
                                
                                st.session_state.processed_audios.clear()
                                st.session_state.recordings = audio_service.get_all_recordings()
                                st.session_state.chat_enabled = False
                                show_success(f"{deleted_count} audio(s) eliminado(s) exitosamente")
                                st.rerun()
                            except Exception as e:
                                show_error(f"Error en eliminación: {str(e)}")
    else:
        show_info("No hay audios guardados. Sube un archivo.")

# SECCIÓN DE TRANSCRIPCIÓN

if st.session_state.get("chat_enabled", False) and st.session_state.get("contexto"):
    st.header("Transcripción del Audio")
    st.caption(f"De: {st.session_state.get('selected_audio', 'audio')}")
    
    with st.container(border=True):
        st.text_area("", st.session_state.contexto, height=200, disabled=True, label_visibility="collapsed")
    
    st.subheader("Palabras Clave Contextualizadas")
    st.caption("Añade palabras clave para que la IA las entienda mejor")
    
    col_kw1, col_kw2, col_kw3 = st.columns([1.5, 1.5, 1])
    with col_kw1:
        new_keyword = st.text_input("Palabra clave:", placeholder="Ej: presupuesto")
    with col_kw2:
        keyword_context = st.text_input("Contexto/Descripción:", placeholder="Ej: total de $5000")
    with col_kw3:
        if st.button("Anadir", use_container_width=True):
            if new_keyword:
                st.session_state.keywords[new_keyword] = keyword_context if keyword_context else "Sin descripción"
                show_success(f"'{new_keyword}' añadida")
                st.rerun()
    
    if st.session_state.keywords:
        st.write("**Palabras clave configuradas:**")
        for keyword, context in st.session_state.keywords.items():
            col_display = st.columns([0.5, 2, 2, 0.3])
            with col_display[0]:
                st.write("[TAG]")
            with col_display[1]:
                st.write(f"**{keyword}**")
            with col_display[2]:
                st.write(f"_{context}_")
            with col_display[3]:
                if st.button("X", key=f"del_{keyword}"):
                    del st.session_state.keywords[keyword]
                    st.rerun()
        
        if st.button("Analizar y Generar Tickets de Oportunidades", use_container_width=True, type="primary"):
            with st.spinner("Analizando transcripción..."):
                keywords_list = list(st.session_state.keywords.keys())
                opportunities = opportunity_service.extract_opportunities(
                    st.session_state.contexto,
                    keywords_list
                )
                
                saved_count = 0
                for opp in opportunities:
                    opportunity_service.save(opp, st.session_state.selected_audio)
                    saved_count += 1
                
                if saved_count > 0:
                    show_success(f"{saved_count} ticket(s) de oportunidad generado(s)")
                    st.session_state.show_opportunities = True
                    st.rerun()
                else:
                    show_warning("No se encontraron oportunidades con las palabras clave")

# SECCIÓN DE OPORTUNIDADES

if st.session_state.get("chat_enabled", False):
    selected_audio = st.session_state.get("selected_audio", "")
    opportunities = opportunity_service.get_all() if selected_audio else []
    
    if opportunities:
        st.header("Tickets de Oportunidades de Negocio")
        
        for idx, opp in enumerate(opportunities):
            title = opp.get('title', 'Sin título')
            with st.expander(f"{title}", expanded=False):
                col_opp1, col_opp2 = st.columns([2, 1])
                
                with col_opp1:
                    st.markdown("<div class='ticket-label' style='color: #ef4444; text-transform: none; margin-top: 0;'>Contexto encontrado en el audio</div>", unsafe_allow_html=True)
                    description = opp.get('description', '')
                    st.markdown(f"""
                    <div class="notification-container notification-info">
                        {description}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    new_notes = st.text_area(
                        "Notas y resumen",
                        value=opp.get('notes', ''),
                        placeholder="Escribe el resumen de esta oportunidad de negocio...",
                        height=100,
                        key=f"notes_{idx}",
                        label_visibility="visible"
                    )
                
                with col_opp2:
                    st.markdown("<div class='ticket-label'>Estado</div>", unsafe_allow_html=True)
                    status_options = ["new", "in_progress", "closed", "won"]
                    status = opp.get('status', 'new')
                    try:
                        status_index = status_options.index(status)
                    except ValueError:
                        status_index = 0
                    
                    new_status = st.selectbox(
                        "Estado",
                        status_options,
                        index=status_index,
                        key=f"status_{idx}",
                        label_visibility="collapsed"
                    )
                    
                    st.markdown("<div class='ticket-label' style='margin-top: 16px;'>Prioridad</div>", unsafe_allow_html=True)
                    priority_options = ["Low", "Medium", "High"]
                    priority = opp.get('priority', 'Medium')
                    try:
                        priority_index = priority_options.index(priority)
                    except ValueError:
                        priority_index = 1
                    
                    new_priority = st.selectbox(
                        "Prioridad",
                        priority_options,
                        index=priority_index,
                        key=f"priority_{idx}",
                        label_visibility="collapsed"
                    )
                
                col_save, col_delete = st.columns(2)
                with col_save:
                    if st.button("Guardar cambios", key=f"save_{idx}", use_container_width=True):
                        opp['notes'] = new_notes
                        opp['status'] = new_status
                        opp['priority'] = new_priority
                        if opportunity_service.update(opp):
                            show_success("Cambios guardados")
                            st.rerun()
                        else:
                            show_error("Error al guardar")
                
                with col_delete:
                    if st.button("Eliminar", key=f"delete_{idx}", use_container_width=True):
                        if opportunity_service.delete(opp.get('id')):
                            show_success("Oportunidad eliminada")
                            st.rerun()
                        else:
                            show_error("Error al eliminar")

# SECCIÓN DE CHAT

if st.session_state.get("chat_enabled", False):
    st.header("Asistente IA para Análisis de Reuniones")
    st.caption(f"Conversando sobre: {st.session_state.get('selected_audio', 'audio')}")
    
    if st.session_state.get("keywords"):
        show_info(f"Palabras clave activas: {', '.join(st.session_state.keywords.keys())}")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if st.session_state.chat_history:
        st.markdown("""<div class="chat-container">""", unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            if message.startswith("Usuario:"):
                user_text = message.replace("Usuario: ", "")
                st.markdown(f"""
                <div class="chat-message chat-message-user">
                    <div class="chat-avatar chat-avatar-user avatar-pulse">U</div>
                    <div class="chat-bubble chat-bubble-user">{user_text}</div>
                </div>
                """, unsafe_allow_html=True)
            elif message.startswith("IA:"):
                ai_text = message.replace("IA: ", "")
                st.markdown(f"""
                <div class="chat-message chat-message-ai">
                    <div class="chat-avatar chat-avatar-ai avatar-spin">A</div>
                    <div class="chat-bubble chat-bubble-ai">{ai_text}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    col_left, col_input, col_right = st.columns([1, 3, 1])
    with col_input:
        user_input = st.chat_input("Escribe tu pregunta o solicitud de análisis...")
    
    if user_input:
        st.session_state.chat_history.append(f"Usuario: {user_input}")
        
        with st.spinner("Generando respuesta..."):
            try:
                keywords = st.session_state.get("keywords", {})
                response = chat_model.call_model(user_input, st.session_state.contexto, keywords)
                st.session_state.chat_history.append(f"IA: {response}")
                st.rerun()
            except Exception as e:
                show_error(f"Error al generar respuesta: {e}")
else:
    show_info("Carga un audio y transcríbelo para habilitar el chat.")

# SECCIÓN DEBUG
with st.expander("DEBUG - Estado de Supabase"):
    show_info_expanded("Probando conexion a Supabase...")
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            test = supabase.table("recordings").select("*", count="exact").execute()
            record_count = len(test.data) if test.data else 0
            
            test_opp = supabase.table("opportunities").select("*", count="exact").execute()
            opp_count = len(test_opp.data) if test_opp.data else 0
            
            test_trans = supabase.table("transcriptions").select("*", count="exact").execute()
            trans_count = len(test_trans.data) if test_trans.data else 0
            
            show_success_expanded("[OK] Conexion establecida correctamente!")
            show_success_expanded(f"Grabaciones en BD: {record_count}")
            show_success_expanded(f"Oportunidades en BD: {opp_count}")
            show_success_expanded(f"Transcripciones en BD: {trans_count}")
        else:
            show_error_expanded("[ERROR] Falta SUPABASE_URL o SUPABASE_KEY en Secrets")
            
    except Exception as e:
        show_error_expanded(f"[ERROR] {str(e)}")
        show_info_expanded("Soluciones:")
        st.write("1. Verifica secretos en Streamlit Cloud")
        st.write("2. Haz 'Reboot app' desde el menu")
        st.write("3. Verifica que no haya espacios en las claves")
