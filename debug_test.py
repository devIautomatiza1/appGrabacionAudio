# Test de debug para Streamlit

import streamlit as st
import os
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

st.title("🔧 TEST: Debug de Extracción de Audios")

st.info("Este test verifica si la función get_recordings_from_supabase() está funcionando correctamente")

# Paso 1: Verificar que tenemos credenciales
st.subheader("Paso 1: Verificar credenciales en Streamlit")
try:
    supabase_url = st.secrets.get("SUPABASE_URL")
    supabase_key = st.secrets.get("SUPABASE_KEY")
    
    if supabase_url:
        st.success(f"✅ SUPABASE_URL: {supabase_url[:40]}...")
    else:
        st.error("❌ SUPABASE_URL no encontrada en secrets")
    
    if supabase_key:
        st.success(f"✅ SUPABASE_KEY: {supabase_key[:30]}...")
    else:
        st.error("❌ SUPABASE_KEY no encontrada en secrets")
except Exception as e:
    st.error(f"❌ Error: {e}")

# Paso 2: Intentar conexión directa a Supabase
st.subheader("Paso 2: Conexión a Supabase")
try:
    from supabase import create_client
    
    supabase_url = st.secrets.get("SUPABASE_URL")
    supabase_key = st.secrets.get("SUPABASE_KEY")
    
    client = create_client(supabase_url.strip(), supabase_key.strip())
    st.success("✅ Cliente Supabase creado correctamente")
    
    # Paso 3: Query a tabla recordings
    st.subheader("Paso 3: SELECT * FROM recordings")
    response = client.table("recordings").select("*").execute()
    
    if response.data:
        st.success(f"✅ {len(response.data)} audios encontrados")
        for i, record in enumerate(response.data, 1):
            with st.expander(f"Audio #{i}: {record.get('filename')}"):
                st.json(record)
    else:
        st.warning("⚠️ No hay audios en la tabla")
    
    # Paso 4: Query filenames ordenado
    st.subheader("Paso 4: SELECT filename ORDER BY created_at DESC")
    response = client.table("recordings").select("filename").order("created_at", desc=True).execute()
    
    if response.data:
        filenames = [record["filename"] for record in response.data]
        st.success(f"✅ Filenames: {filenames}")
    else:
        st.warning("⚠️ Sin datos")
    
except ImportError as e:
    st.error(f"❌ Error de importación: {e}")
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.write(str(e))

# Paso 5: Probar la función AudioRecorder
st.subheader("Paso 5: Llamar a AudioRecorder.get_recordings_from_supabase()")
try:
    from AudioRecorder import AudioRecorder
    recorder = AudioRecorder()
    recordings = recorder.get_recordings_from_supabase()
    st.success(f"✅ Función ejecutada correctamente")
    st.write(f"Audios retornados: {recordings}")
except Exception as e:
    st.error(f"❌ Error: {e}")
    import traceback
    st.write(traceback.format_exc())

st.divider()
st.info("💡 Si ves audios en los pasos 3 y 4 pero no en Paso 5, el problema está en AudioRecorder")
st.info("💡 Si no ves audios en ningún lado, el problema está en Supabase o credenciales")
