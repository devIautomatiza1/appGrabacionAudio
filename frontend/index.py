import streamlit as st
import sys, re
from pathlib import Path
from datetime import datetime

# Configuración de Paths y Módulos
app_root = Path(__file__).parent.parent
for folder in ["backend", "frontend"]:
    sys.path.insert(0, str(app_root / folder))

from config import APP_NAME, AUDIO_EXTENSIONS, CHAT_HISTORY_LIMIT
from logger import get_logger
import styles, database as db_utils
from AudioRecorder import AudioRecorder
from Transcriber import Transcriber
from Model import Model
from OpportunitiesManager import OpportunitiesManager
from notifications import *
from utils import process_audio_file, delete_audio
from performance import *
from helpers import format_recording_name

# --- INICIALIZACIÓN ---
st.set_page_config(layout="wide", page_title=APP_NAME)
st.markdown(styles.get_styles(), unsafe_allow_html=True)
logger = get_logger(__name__)

# Instancias de clases
recorder, transcriber, chat_model, opp_manager = AudioRecorder(), Transcriber(), Model(), OpportunitiesManager()

if "recordings" not in st.session_state:
    st.session_state.update({
        "processed_audios": set(), "recordings": recorder.get_recordings_from_supabase(),
        "selected_audio": None, "upload_key_counter": 0, "record_key_counter": 0,
        "keywords": {}, "delete_confirmation": {}, "transcription_cache": {},
        "opp_delete_confirmation": {}, "debug_log": []
    })
init_optimization_state()

def add_debug_event(msg, type="info"):
    st.session_state.debug_log.append({"time": datetime.now().strftime("%H:%M:%S"), "type": type, "message": msg})

st.title(APP_NAME)

# --- CARGA DE AUDIO ---
col1, col2 = st.columns(2)
with col1:
    st.markdown('<h3 style="color: white;">Grabadora y Carga</h3>', unsafe_allow_html=True)
    
    # Grabadora Nativa
    audio_in = st.audio_input("Grabar:", key=f"rec_{st.session_state.record_key_counter}")
    if audio_in:
        fname = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        if process_audio_file(audio_in.getvalue(), fname, recorder, db_utils)[0]:
            st.session_state.record_key_counter += 1
            st.rerun()

    # Subida de Archivo
    uploaded = st.file_uploader("Subir:", type=list(AUDIO_EXTENSIONS), key=f"up_{st.session_state.upload_key_counter}")
    if uploaded:
        if process_audio_file(uploaded.read(), uploaded.name, recorder, db_utils)[0]:
            st.session_state.upload_key_counter += 1
            st.rerun()

# --- GESTIÓN DE AUDIOS ---
with col2:
    st.markdown('<h3 style="color: white;">Audios Guardados</h3>', unsafe_allow_html=True)
    recs = recorder.get_recordings_from_supabase()
    st.session_state.recordings = recs
    
    if recs:
        search = st.text_input("🔍 Buscar:", placeholder="Filtrar por nombre...")
        filtered = [r for r in recs if re.escape(search.lower()) in r.lower()] if search else recs
        
        tab1, tab2 = st.tabs(["Transcribir", "Lotes"])
        with tab1:
            sel = st.selectbox("Selecciona audio:", filtered, format_func=lambda x: f"{format_recording_name(x)} {'✓' if is_audio_transcribed(x, db_utils) else ''}")
            
            if sel and sel != st.session_state.get("loaded_audio"):
                data = db_utils.get_transcription_by_filename(sel)
                st.session_state.update({"contexto": data["content"] if data else None, "selected_audio": sel, "loaded_audio": sel, "chat_enabled": bool(data)})

            c_play, c_trans, c_del = st.columns(3)
            if c_play.button("▶️ Reproducir"):
                st.audio(recorder.get_recording_path(sel))
            
            if c_trans.button("✍️ Transcribir"):
                with st.spinner("Procesando..."):
                    txt = transcriber.transcript_audio(recorder.get_recording_path(sel)).text
                    db_utils.save_transcription(sel, txt, "es")
                    st.session_state.update({"contexto": txt, "chat_enabled": True})
                    st.rerun()

            if c_del.button("🗑️ Eliminar"):
                st.session_state.delete_confirmation[sel] = True

            if st.session_state.delete_confirmation.get(sel):
                if st.button(f"⚠️ Confirmar eliminar {sel}"):
                    if delete_audio(sel, recorder, db_utils):
                        delete_recording_local(sel)
                        st.session_state.update({"chat_enabled": False, "selected_audio": None})
                        st.rerun()

# --- TRANSCRIPCIÓN Y KEYWORDS ---
if st.session_state.get("chat_enabled") and st.session_state.get("contexto"):
    st.divider()
    st.subheader("Transcripción")
    st.text_area("", st.session_state.contexto, height=150, disabled=True)
    
    st.subheader("Análisis de Oportunidades")
    kw_col1, kw_col2 = st.columns([3, 1])
    new_kw = kw_col1.text_input("Nueva palabra clave:", key="kw_input")
    if kw_col2.button("Añadir") and new_kw:
        st.session_state.keywords[new_kw.strip().lower()] = new_kw.strip().lower()
        st.rerun()

    # Visualización de Keywords
    for kw in list(st.session_state.keywords.keys()):
        cols = st.columns([5, 1])
        cols[0].info(f"Key: {kw}")
        if cols[1].button("X", key=f"del_kw_{kw}"):
            delete_keyword_local(kw)
            st.rerun()

    if st.button("🚀 Analizar y Generar Tickets", use_container_width=True):
        with st.spinner("Buscando oportunidades..."):
            opps = opp_manager.extract_opportunities(st.session_state.contexto, list(st.session_state.keywords.keys()))
            for o in opps: opp_manager.save_opportunity(o, st.session_state.selected_audio)
            show_success(f"Se generaron {len(opps)} tickets")
            st.rerun()

# --- TICKETS Y CHAT ---
if st.session_state.get("chat_enabled"):
    opps = opp_manager.load_opportunities(st.session_state.selected_audio)
    if opps:
        st.header("Tickets Encontrados")
        for i, opp in enumerate(opps):
            with st.expander(f"📌 {opp['keyword']} - {opp['created_at']}"):
                st.write(opp['full_context'])
                # Lógica simplificada de guardado/eliminación de tickets aquí...

    st.header("Asistente IA")
    for msg in st.session_state.get("chat_history", []):
        with st.chat_message("user" if "Usuario" in msg else "assistant"):
            st.write(msg.split(": ", 1)[1])

    if prompt := st.chat_input("Pregunta sobre la reunión..."):
        if "chat_history" not in st.session_state: st.session_state.chat_history = []
        st.session_state.chat_history.append(f"👤 Usuario: {prompt}")
        res = chat_model.call_model(prompt, st.session_state.contexto, st.session_state.keywords)
        st.session_state.chat_history.append(f"🤖 IA: {res}")
        st.rerun()