import streamlit as st
import os
import AudioRecorder
import Transcriber
import Model
# Force redeploy with updated credentials - 2026-02-05
import OpportunitiesManager
from datetime import datetime
import hashlib
import database as db_utils

# 🎨 DISEÑO MODERNO - IMPORTAR
from modern_ui import (
    inject_modern_css,
    success_toast,
    error_toast,
    warning_toast,
    info_toast
)

# Configuración inicial de la interfaz de usuario
st.set_page_config(layout="wide", page_title="🎙️ AudioPro Intelligence")

# ✅ INYECTAR CSS MODERNO PRIMERO (MUY IMPORTANTE)
inject_modern_css()

# Inicializar objetos
recorder = AudioRecorder.AudioRecorder()
transcriber_model = Transcriber.Transcriber()
chat_model = Model.Model()
opp_manager = OpportunitiesManager.OpportunitiesManager()

# Inicializar estado de sesión
if "processed_audios" not in st.session_state:
    st.session_state.processed_audios = set()  # Audios ya procesados
if "recordings" not in st.session_state:
    st.session_state.recordings = recorder.get_recordings_from_supabase()
if "is_deleting" not in st.session_state:
    st.session_state.is_deleting = False
if "selected_audio" not in st.session_state:
    st.session_state.selected_audio = None
if "upload_key_counter" not in st.session_state:
    st.session_state.upload_key_counter = 0
if "record_key_counter" not in st.session_state:
    st.session_state.record_key_counter = 0

# ============================================================================
# ENCABEZADO CON ESTILO MODERNO
# ============================================================================

st.markdown("""
<div style="text-align: center; margin: 2rem 0; padding: 2rem;">
    <h1 style="font-size: 3rem; margin: 0;">🎙️ AudioPro</h1>
    <p style="color: #B0B8C1; font-size: 1.1rem; margin-top: 0.5rem;">
        Plataforma de IA para Transcripción y Análisis de Audios
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Crear dos columnas principales para la carga
col1, col2 = st.columns([1, 1])

with col1:
    # GRABADORA DE AUDIO EN VIVO (nativa de Streamlit)
    st.markdown('<h3 style="color: white;">Grabadora en vivo</h3>', unsafe_allow_html=True)
    st.caption("Graba directamente desde tu micrófono (sin interrupciones)")
    
    audio_data = st.audio_input("Presiona el botón para grabar:", key=f"audio_recorder_{st.session_state.record_key_counter}")
    
    # Procesar audio grabado SOLO UNA VEZ por hash
    if audio_data is not None:
        audio_bytes = audio_data.getvalue()
        if len(audio_bytes) > 0:
            audio_hash = hashlib.md5(audio_bytes).hexdigest()
            
            # Verificar: ¿Es un audio que ya procesamos?
            if audio_hash not in st.session_state.processed_audios:
                try:
                    # Guardar el audio grabado
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"recording_{timestamp}.wav"
                    filepath = recorder.save_recording(audio_bytes, filename)
                    
                    # Guardar en Supabase
                    recording_id = db_utils.save_recording_to_db(filename, filepath)
                    
                    # CLAVE: Marcar como procesado ANTES de mostrar mensaje
                    st.session_state.processed_audios.add(audio_hash)
                    
                    # Actualizar lista desde Supabase
                    st.session_state.recordings = recorder.get_recordings_from_supabase()
                    
                    success_toast(f"Audio '{filename}' grabado y guardado")
                    
                    # Reset el widget para que no se procese nuevamente
                    st.session_state.record_key_counter += 1
                    
                except Exception as e:
                    error_toast(f"Error al grabar: {str(e)}")
    
    st.divider()
    
    # Opción de subir archivo
    st.markdown('<h3 style="color: white;">Sube un archivo de audio</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Selecciona un archivo de audio", type=["mp3", "wav", "m4a", "ogg", "flac", "webm"], key=f"audio_uploader_{st.session_state.upload_key_counter}")
    
    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        if len(audio_bytes) > 0:
            audio_hash = hashlib.md5(audio_bytes).hexdigest()
            
            # Verificar: ¿Es un archivo que ya procesamos?
            if audio_hash not in st.session_state.processed_audios:
                try:
                    filename = uploaded_file.name
                    filepath = recorder.save_recording(audio_bytes, filename)
                    
                    # Guardar en Supabase
                    recording_id = db_utils.save_recording_to_db(filename, filepath)
                    
                    # CLAVE: Marcar como procesado ANTES de mostrar mensaje
                    st.session_state.processed_audios.add(audio_hash)
                    
                    # Actualizar lista desde Supabase
                    st.session_state.recordings = recorder.get_recordings_from_supabase()
                    
                    success_toast(f"Archivo '{filename}' cargado y guardado")
                    
                    # Reset el widget para que no se procese nuevamente
                    st.session_state.upload_key_counter += 1
                    
                except Exception as e:
                    error_toast(f"Error al cargar: {str(e)}")

with col2:
    st.markdown('<h3 style="color: white;">Audios Guardados</h3>', unsafe_allow_html=True)
    
    # Refresh de la lista de audios desde Supabase cada vez que se renderiza (para sincronizar)
    recordings = recorder.get_recordings_from_supabase()
    st.session_state.recordings = recordings
    
    if recordings:
        # Métrica de audios guardados
        
        # Tabs para diferentes vistas
        tab1, tab2 = st.tabs(["Transcribir", "Gestión en lote"])
        
        with tab1:
            selected_audio = st.selectbox(
                "Selecciona un audio para transcribir",
                recordings,
                format_func=lambda x: x.replace("_", " ").replace(".wav", "").replace(".mp3", "").replace(".m4a", "").replace(".webm", "").replace(".ogg", "").replace(".flac", "")
            )
            
            if selected_audio:
                # Cargar transcripción existente automáticamente si existe
                if selected_audio != st.session_state.get("loaded_audio"):
                    existing_transcription = db_utils.get_transcription_by_filename(selected_audio)
                    if existing_transcription:
                        st.session_state.contexto = existing_transcription["content"]
                        st.session_state.selected_audio = selected_audio
                        st.session_state.loaded_audio = selected_audio
                        st.session_state.chat_enabled = True
                        st.session_state.keywords = {}
                        info_toast("Transcripción cargada desde Supabase")
                
                col_play, col_transcribe, col_delete = st.columns([1, 1, 1])
                
                with col_play:
                    if st.button("Reproducir"):
                        audio_path = recorder.get_recording_path(selected_audio)
                        extension = selected_audio.split('.')[-1]
                        with open(audio_path, "rb") as f:
                            st.audio(f.read(), format=f"audio/{extension}")
                
                with col_transcribe:
                    if st.button("Transcribir"):
                        with st.spinner("Transcribiendo..."):
                            try:
                                audio_path = recorder.get_recording_path(selected_audio)
                                transcription = transcriber_model.transcript_audio(audio_path)
                                st.session_state.contexto = transcription.text
                                st.session_state.selected_audio = selected_audio
                                st.session_state.loaded_audio = selected_audio
                                st.session_state.chat_enabled = True
                                st.session_state.keywords = {}
                                
                                # Guardar la transcripción en Supabase
                                transcription_id = db_utils.save_transcription(
                                    recording_filename=selected_audio,
                                    content=transcription.text,
                                    language="es"
                                )
                                
                                success_toast("Transcripción completada y guardada")
                            except Exception as e:
                                error_toast(f"Error al transcribir: {e}")
                
                with col_delete:
                    if st.button("Eliminar", key=f"delete_{selected_audio}"):
                        try:
                            # Eliminar de Supabase
                            db_utils.delete_recording_by_filename(selected_audio)
                            # Eliminar localmente
                            recorder.delete_recording(selected_audio)
                            # Limpiar processed_audios para permitir re-agregar si es necesario
                            st.session_state.processed_audios.clear()
                            
                            st.session_state.recordings = recorder.get_recordings_from_supabase()
                            st.session_state.chat_enabled = False
                            st.session_state.loaded_audio = None
                            success_toast("Audio eliminado correctamente")
                            st.rerun()
                        except Exception as e:
                            error_toast(f"Error al eliminar: {str(e)}")
        
        with tab2:
            st.subheader("Eliminar múltiples audios")
            st.write("Selecciona uno o varios audios para eliminarlos")
            
            audios_to_delete = st.multiselect(
                "Audios a eliminar:",
                recordings,
                format_func=lambda x: x.replace("_", " ").replace(".wav", "").replace(".mp3", "").replace(".m4a", "").replace(".webm", "").replace(".ogg", "").replace(".flac", "")
            )
            
            if audios_to_delete:
                warning_toast(f"Vas a eliminar {len(audios_to_delete)} audio(s)")
                
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
                                    # Eliminar de Supabase
                                    db_utils.delete_recording_by_filename(audio)
                                    # Eliminar localmente
                                    recorder.delete_recording(audio)
                                    deleted_count += 1
                                except Exception as e:
                                    error_toast(f"Error al eliminar {audio}: {e}")
                            
                            # Limpiar processed_audios para permitir re-agregar
                            st.session_state.processed_audios.clear()
                            st.session_state.recordings = recorder.get_recordings_from_supabase()
                            st.session_state.chat_enabled = False
                            success_toast(f"{deleted_count} audio(s) eliminado(s)")
                            st.rerun()
                        except Exception as e:
                            error_toast(f"Error en eliminación: {str(e)}")
                
                with col_cancel:
                    st.write("")
    else:
        st.info("📭 No hay audios guardados. Carga uno para comenzar.")

# SECCIÓN DE TRANSCRIPCIÓN
st.divider()

if st.session_state.get("chat_enabled", False) and st.session_state.get("contexto"):
    st.header("Transcripción del Audio")
    st.caption(f"De: {st.session_state.get('selected_audio', 'audio')}")
    
    # Mostrar transcripción en un contenedor
    with st.container(border=True):
        st.text_area("", st.session_state.contexto, height=200, disabled=True, label_visibility="collapsed")
    
    # SECCIÓN DE PALABRAS CLAVE
    st.subheader("Palabras Clave Contextualizadas")
    st.caption("Añade palabras clave para que la IA las entienda mejor")
    
    col_kw1, col_kw2, col_kw3 = st.columns([1.5, 1.5, 1])
    with col_kw1:
        new_keyword = st.text_input("Palabra clave:", placeholder="Ej: presupuesto")
    with col_kw2:
        keyword_context = st.text_input("Contexto/Descripción:", placeholder="Ej: total de $5000")
    with col_kw3:
        if st.button("➕ Añadir", use_container_width=True):
            if new_keyword:
                st.session_state.keywords[new_keyword] = keyword_context if keyword_context else "Sin descripción"
                success_toast(f"'{new_keyword}' agregada")
                st.rerun()
    
    # Mostrar palabras clave
    if st.session_state.keywords:
        st.write("**📌 Palabras clave configuradas:**")
        for keyword, context in st.session_state.keywords.items():
            col_display = st.columns([0.5, 2, 2, 0.3])
            with col_display[0]:
                st.write("🏷️")
            with col_display[1]:
                st.write(f"**{keyword}**")
            with col_display[2]:
                st.write(f"_{context}_")
            with col_display[3]:
                if st.button("✖️", key=f"del_{keyword}"):
                    del st.session_state.keywords[keyword]
                    st.rerun()
        
        # Botón para generar oportunidades
        st.divider()
        if st.button("🎯 Analizar y Generar Tickets de Oportunidades", use_container_width=True, type="primary"):
            with st.spinner("Analizando transcripción..."):
                keywords_list = list(st.session_state.keywords.keys())
                opportunities = opp_manager.extract_opportunities(
                    st.session_state.contexto,
                    keywords_list
                )
                
                saved_count = 0
                for opp in opportunities:
                    opp_manager.save_opportunity(opp, st.session_state.selected_audio)
                    saved_count += 1
                
                if saved_count > 0:
                    success_toast(f"{saved_count} ticket(s) de oportunidad generado(s)")
                    st.session_state.show_opportunities = True
                    st.rerun()
                else:
                    warning_toast("No se encontraron oportunidades con las palabras clave")

# SECCIÓN DE OPORTUNIDADES
st.divider()

if st.session_state.get("chat_enabled", False):
    selected_audio = st.session_state.get("selected_audio", "")
    opportunities = opp_manager.load_opportunities(selected_audio)
    
    if opportunities:
        st.header("🎟️ Tickets de Oportunidades de Negocio")
        
        for idx, opp in enumerate(opportunities):
            # Mostrar número de ocurrencia si hay múltiples
            occurrence_text = ""
            if opp.get('occurrence', 1) > 1:
                occurrence_text = f" (Ocurrencia #{opp['occurrence']})"
            
            with st.expander(f"📌 {opp['keyword']}{occurrence_text} - {opp['created_at']}", expanded=False):
                col_opp1, col_opp2 = st.columns([2, 1])
                
                with col_opp1:
                    st.write("**Contexto encontrado en el audio:**")
                    st.markdown(f"<div style='background: rgba(0,251,255,0.1); padding: 12px; border-radius: 8px; border-left: 3px solid #00FBFF; color: #B0B8C1;'>{opp['full_context']}</div>", unsafe_allow_html=True)
                    
                    new_notes = st.text_area(
                        "Notas y resumen:",
                        value=opp.get('notes', ''),
                        placeholder="Escribe el resumen de esta oportunidad de negocio...",
                        height=100,
                        key=f"notes_{idx}"
                    )
                
                with col_opp2:
                    st.write("**Estado:**")
                    status_options = ["new", "in_progress", "closed", "won"]
                    new_status = st.selectbox(
                        "Cambiar estado",
                        status_options,
                        index=status_options.index(opp.get('status', 'new')),
                        key=f"status_{idx}",
                        label_visibility="collapsed"
                    )
                    
                    st.write("**Prioridad:**")
                    priority_options = ["Low", "Medium", "High"]
                    new_priority = st.selectbox(
                        "Cambiar prioridad",
                        priority_options,
                        index=priority_options.index(opp.get('priority', 'Medium')),
                        key=f"priority_{idx}",
                        label_visibility="collapsed"
                    )
                
                col_save, col_delete = st.columns(2)
                with col_save:
                    if st.button("💾 Guardar cambios", key=f"save_{idx}", use_container_width=True):
                        opp['notes'] = new_notes
                        opp['status'] = new_status
                        opp['priority'] = new_priority
                        if opp_manager.update_opportunity(opp, selected_audio):
                            success_toast("Cambios guardados")
                            st.rerun()
                        else:
                            error_toast("Error al guardar")
                
                with col_delete:
                    if st.button("🗑️ Eliminar", key=f"delete_{idx}", use_container_width=True):
                        if opp_manager.delete_opportunity(opp['id'], selected_audio):
                            success_toast("Eliminado")
                            st.rerun()
                        else:
                            error_toast("Error al eliminar")

# SECCIÓN DE CHAT
st.divider()

if st.session_state.get("chat_enabled", False):
    st.header("💬 Chat con IA")
    st.caption(f"Conversando sobre: {st.session_state.get('selected_audio', 'audio')}")
    
    # Mostrar palabras clave activas
    if st.session_state.get("keywords"):
        keywords_text = ", ".join(st.session_state.keywords.keys())
        st.info(f"🏷️ Palabras clave activas: {keywords_text}")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Mostrar historial de chat
    for message in st.session_state.chat_history:
        st.write(message)
    
    # Campo de entrada
    user_input = st.chat_input("Escribe tu pregunta sobre el audio:")
    
    if user_input:
        st.session_state.chat_history.append(f"👤 **Usuario**: {user_input}")
        
        with st.spinner("Generando respuesta..."):
            try:
                # Pasar palabras clave al modelo
                keywords = st.session_state.get("keywords", {})
                response = chat_model.call_model(user_input, st.session_state.contexto, keywords)
                st.session_state.chat_history.append(f"🤖 **IA**: {response}")
                st.rerun()
            except Exception as e:
                error_toast(f"Error: {e}")
else:
    st.info("👆 Carga un audio, transcríbelo y agrega palabras clave para activar todas las funciones.")

# SECCIÓN DEBUG
st.divider()
with st.expander("🔧 Monitor del Sistema", expanded=False):
    st.info("📊 Estado de Supabase y estadísticas generales")
    
    try:
        # Usar el cliente que ya tenemos en database.py
        supabase = db_utils.init_supabase()
        
        if supabase:
            # Contar grabaciones
            test = supabase.table("recordings").select("*", count="exact").execute()
            record_count = len(test.data) if test.data else 0
            
            # Contar oportunidades
            test_opp = supabase.table("opportunities").select("*", count="exact").execute()
            opp_count = len(test_opp.data) if test_opp.data else 0
            
            # Contar transcripciones
            test_trans = supabase.table("transcriptions").select("*", count="exact").execute()
            trans_count = len(test_trans.data) if test_trans.data else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Grabaciones", record_count, "🎵")
            with col2:
                st.metric("Oportunidades", opp_count, "📋")
            with col3:
                st.metric("Transcripciones", trans_count, "📝")
            
            success_toast("Conexión a Supabase establecida")
        else:
            error_toast("Falta configuración en Secrets")
            
    except Exception as e:
        error_toast(f"Error de conexión: {str(e)}")