"""
Debug page - Diagnosticar extracción de audios desde Supabase
Accesible desde el menú de Streamlit como una pestaña adicional
"""
import streamlit as st
from supabase import create_client

st.title("🔧 DEBUG: Extracción de Audios desde Supabase")

st.info("Esta página diagnostica por qué no aparecen los audios del desplegable")

# Paso 1: Verificar credenciales
st.subheader("✅ Paso 1: Verificar credenciales")
col1, col2 = st.columns(2)

with col1:
    supabase_url = st.secrets.get("SUPABASE_URL")
    if supabase_url:
        st.success(f"SUPABASE_URL: {supabase_url[:45]}...")
    else:
        st.error("SUPABASE_URL NO encontrada")

with col2:
    supabase_key = st.secrets.get("SUPABASE_KEY")
    if supabase_key:
        st.success(f"SUPABASE_KEY: {supabase_key[:45]}...")
    else:
        st.error("SUPABASE_KEY NO encontrada")

# Paso 2: Conectar a Supabase
st.subheader("✅ Paso 2: Conectar a Supabase")
try:
    client = create_client(
        st.secrets.get("SUPABASE_URL").strip(),
        st.secrets.get("SUPABASE_KEY").strip()
    )
    st.success("✅ Conexión establecida")
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.stop()

# Paso 3: Verificar tabla recordings
st.subheader("✅ Paso 3: Leer tabla 'recordings'")
try:
    response = client.table("recordings").select("*").execute()
    
    if response.data:
        st.success(f"✅ Encontrados {len(response.data)} audios")
        
        # Mostrar tabla
        st.dataframe(response.data)
        
        # Mostrar detalles
        with st.expander("Ver detalles de cada audio"):
            for i, record in enumerate(response.data, 1):
                st.write(f"\n**Audio #{i}:**")
                for key, value in record.items():
                    st.write(f"  • `{key}`: {value}")
    else:
        st.warning("⚠️ No hay audios en la tabla 'recordings'")
        
except Exception as e:
    st.error(f"❌ Error leyendo tabla: {e}")
    st.stop()

# Paso 4: Query específico (el que usa AudioRecorder)
st.subheader("✅ Paso 4: Query específico (filenames ordenados)")
try:
    response = client.table("recordings").select("filename").order("created_at", desc=True).execute()
    
    if response.data:
        filenames = [record["filename"] for record in response.data]
        st.success(f"✅ Filenames retornados:")
        st.code(str(filenames))
    else:
        st.warning("⚠️ Sin datos en esta query")
except Exception as e:
    st.error(f"❌ Error: {e}")

# Paso 5: Probar AudioRecorder directamente
st.subheader("✅ Paso 5: Probar AudioRecorder.get_recordings_from_supabase()")
try:
    from AudioRecorder import AudioRecorder
    
    recorder = AudioRecorder()
    recordings = recorder.get_recordings_from_supabase()
    
    st.success("✅ Función ejecutada")
    st.code(f"Resultado: {recordings}")
    
    if recordings:
        st.info(f"✅ Se retornaron {len(recordings)} audios")
    else:
        st.warning("⚠️ La función retornó lista vacía")
        
except Exception as e:
    st.error(f"❌ Error: {e}")
    import traceback
    st.write(traceback.format_exc())

# Paso 6: Verificar session_state
st.subheader("✅ Paso 6: Estado de session_state en index.py")
st.info("Cuando abras `index.py` para grabar audios, deberías ver aquí el contenido de st.session_state.recordings")
st.code("""
# En index.py, busca esta línea:
recordings = recorder.get_recordings_from_supabase()
st.session_state.recordings = recordings
""")

st.divider()

st.markdown("""
## 📊 Diagnóstico:

| Escenario | Significado | Solución |
|-----------|-------------|----------|
| ✅ Todos los pasos OK pero Paso 5 vacío | AudioRecorder retorna [] pero Supabase tiene datos | El error está silenciado en get_recordings_from_supabase() |
| ✅ Paso 4 con datos, Paso 5 vacío | Las credenciales funcionan en cliente pero no en función | Revisar el try/except de AudioRecorder |
| ❌ Paso 2 falla | No hay conexión a Supabase | Verificar secrets en .streamlit/secrets.toml |
| ⚠️ Paso 3/4 vacío | No hay audios en BD | Sube un audio primero desde index.py |
""")
