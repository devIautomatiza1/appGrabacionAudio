"""example_integration.py - Ejemplo de cómo integrar las nuevas mejoras en index.py"""

# Este es un EJEMPLO de cómo usar las 4 nuevas mejoras
# Copiar y adaptar las secciones que necesites en tu index.py

import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

# ============================================================================
# STEP 1: IMPORTS NUEVOS
# ============================================================================

# ✨ NUEVOS IMPORTS - Caching
from frontend.cached_models import (
    get_transcriber,
    get_chat_model,
    get_audio_recorder,
    get_opportunities_manager
)

# ✨ NUEVO IMPORT - Sentimiento
from backend.sentiment_analyzer import sentiment_analyzer

# ✨ NUEVO IMPORT - Búsqueda avanzada
from backend.advanced_search import searcher

from logger import get_logger
logger = get_logger(__name__)

# ============================================================================
# STEP 2: REEMPLAZAR INICIALIZACIÓN DE MODELOS (línea ~90 en tu index.py)
# ============================================================================

# ❌ ANTES:
# transcriber_model = Transcriber()
# chat_model = Model()
# recorder = AudioRecorder()
# opp_manager = OpportunitiesManager()

# ✅ DESPUÉS:
transcriber_model = get_transcriber()      # ⚡ Cacheado automáticamente
chat_model = get_chat_model()              # ⚡ Cacheado automáticamente
recorder = get_audio_recorder()            # ⚡ Cacheado automáticamente
opp_manager = get_opportunities_manager()  # ⚡ Cacheado automáticamente

# ============================================================================
# EJEMPLO 1: TRANSCRIPCIÓN CON PROGRESS BAR
# ============================================================================

def example_transcription_with_progress():
    """Ejemplo: Transcribir audio con barra de progreso"""
    st.subheader("🎤 Transcribir con Progress Bar")
    
    uploaded_file = st.file_uploader("Selecciona un audio", type=['mp3', 'wav', 'm4a'])
    
    if uploaded_file:
        # Guardar temporalmente
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Crear progress bar
        progress_bar = st.progress(0)
        progress_text = st.empty()
        
        try:
            # Función personalizada que actualiza barra Y texto
            def update_progress(value):
                stages = {
                    0.2: "20% - Validando archivo...",
                    0.4: "40% - Verificando límites...",
                    0.6: "60% - Subiendo a Gemini...",
                    0.8: "80% - Transcribiendo...",
                    1.0: "100% - Completado!"
                }
                closest = min(stages.keys(), key=lambda x: abs(x - value))
                progress_text.write(stages[closest])
                progress_bar.progress(value)
            
            # Transcribir CON progress callback
            result = transcriber_model.transcript_audio(
                temp_path,
                progress_callback=update_progress  # ← Aquí: pasar función
            )
            
            st.success("✓ Transcripción completada!")
            st.text_area("Transcripción:", result.text, height=200)
            
        except RuntimeError as e:
            st.error(f"⚠️  Rate limit excedido: {e}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ============================================================================
# EJEMPLO 2: ANÁLISIS DE SENTIMIENTO
# ============================================================================

def example_sentiment_analysis():
    """Ejemplo: Analizar sentimiento de transcripción"""
    st.subheader("😊 Análisis de Sentimiento")
    
    transcription = st.text_area("Escribe o pega una transcripción:", height=150)
    
    if st.button("Analizar Sentimiento"):
        try:
            st.info("Analizando...")
            sentiment = sentiment_analyzer.analyze(transcription)
            
            # Mostrar resultados en columnas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Color según sentimiento
                if sentiment['sentiment'] == 'positivo':
                    st.metric("📈 Sentimiento", "POSITIVO", "😊")
                elif sentiment['sentiment'] == 'negativo':
                    st.metric("📉 Sentimiento", "NEGATIVO", "😡")
                else:
                    st.metric("➡️ Sentimiento", "NEUTRO", "😐")
            
            with col2:
                st.metric("📊 Confianza", f"{sentiment['score']*100:.1f}%")
            
            with col3:
                st.write("**Emociones detectadas:**")
                for emotion in sentiment['emotions']:
                    st.write(f"• {emotion}")
            
            # Resumen
            st.info(f"📝 **Análisis:** {sentiment['summary']}")
        
        except RuntimeError as e:
            st.error(f"⚠️  Rate limit: {e}")
        except ValueError as e:
            st.error(f"❌ Transcripción inválida: {e}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ============================================================================
# EJEMPLO 3: BÚSQUEDA AVANZADA SIMPLE
# ============================================================================

def example_simple_search():
    """Ejemplo: Búsqueda simple por término"""
    st.subheader("🔍 Búsqueda Simple")
    
    recordings = ["recording_20250211_120000.wav", "meeting_important.wav", "call_client.wav"]
    
    search_query = st.text_input("Buscar grabación:")
    
    if search_query:
        results = searcher.search_transcriptions(recordings, query=search_query)
        st.write(f"**Encontrados:** {len(results)} resultados")
        for r in results:
            st.write(f"✓ {r}")

# ============================================================================
# EJEMPLO 4: BÚSQUEDA AVANZADA CON FILTROS
# ============================================================================

def example_advanced_search():
    """Ejemplo: Búsqueda con filtros de fecha"""
    st.subheader("🔍 Búsqueda Avanzada con Filtros")
    
    recordings = st.session_state.get('recordings', [])
    
    # Búsqueda por término
    search_query = st.text_input("Buscar:", placeholder="cliente, oportunidad, etc...")
    
    # Filtros
    col1, col2 = st.columns(2)
    date_from = col1.date_input("Desde:")
    date_to = col2.date_input("Hasta:")
    
    # Construir filtros
    filters = {}
    if date_from and date_to:
        filters['date_from'] = date_from.strftime('%Y-%m-%d')
        filters['date_to'] = date_to.strftime('%Y-%m-%d')
    
    # Buscar
    results = searcher.search_transcriptions(
        recordings=recordings,
        query=search_query if search_query else "",
        filters=filters if filters else None
    )
    
    st.write(f"**Resultados:** {len(results)}/{len(recordings)}")
    
    # Mostrar en expander
    with st.expander("Ver resultados", expanded=len(results) > 0):
        if results:
            for r in results:
                st.write(f"- {r}")
        else:
            st.info("No se encontraron resultados")

# ============================================================================
# EJEMPLO 5: WORKFLOW COMPLETO
# ============================================================================

def example_complete_workflow():
    """Ejemplo: Workflow completo integrando todas las mejoras"""
    st.title("🚀 Workflow Completo - Todas las Mejoras")
    
    # Tabs para diferentes secciones
    tab1, tab2, tab3 = st.tabs(["Transcribir", "Analizar", "Buscar"])
    
    # === TAB 1: TRANSCRIBIR ===
    with tab1:
        st.subheader("🎤 Paso 1: Transcribir Audio")
        
        uploaded_file = st.file_uploader("Audio:", type=['mp3', 'wav', 'm4a'])
        
        if uploaded_file and st.button("Transcribir"):
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("Procesando..."):
                progress = st.progress(0)
                
                try:
                    # 1. Transcribir
                    result = transcriber_model.transcript_audio(
                        temp_path,
                        progress_callback=progress.progress
                    )
                    st.session_state.transcription = result.text
                    st.success("✓ Completado")
                    
                except Exception as e:
                    st.error(f"Error: {e}")
    
    # === TAB 2: ANALIZAR ===
    with tab2:
        st.subheader("😊 Paso 2: Analizar Sentimiento")
        
        if 'transcription' in st.session_state:
            transcription = st.session_state.transcription
            
            st.text_area("Transcripción:", transcription, height=150, disabled=True)
            
            if st.button("Analizar Sentimiento"):
                try:
                    sentiment = sentiment_analyzer.analyze(transcription)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Sentimiento", sentiment['sentiment'].upper())
                    with col2:
                        st.metric("Score", f"{sentiment['score']:.2f}")
                    with col3:
                        st.write("Emociones:")
                        for e in sentiment['emotions'][:3]:
                            st.write(f"• {e}")
                    
                    st.session_state.sentiment = sentiment
                
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.info("Primero transcribe un audio en la Tab anterior")
    
    # === TAB 3: BUSCAR ===
    with tab3:
        st.subheader("🔍 Paso 3: Buscar en Grabaciones")
        
        recordings = st.session_state.get('recordings', [])
        
        search = st.text_input("Buscar:")
        results = searcher.search_transcriptions(recordings, search)
        
        st.write(f"**Resultados:** {len(results)} de {len(recordings)}")
        for r in results[:10]:
            st.write(f"- {r}")

# ============================================================================
# MAIN - Ejecutar ejemplos
# ============================================================================

if __name__ == "__main__":
    st.set_page_config(page_title="Mejoras - Ejemplos", layout="wide")
    
    # Selector de ejemplo
    example = st.sidebar.selectbox(
        "Selecciona un ejemplo:",
        [
            "Transcripción con Progress",
            "Análisis de Sentimiento",
            "Búsqueda Simple",
            "Búsqueda Avanzada",
            "Workflow Completo"
        ]
    )
    
    # Ejecutar ejemplo seleccionado
    if example == "Transcripción con Progress":
        example_transcription_with_progress()
    elif example == "Análisis de Sentimiento":
        example_sentiment_analysis()
    elif example == "Búsqueda Simple":
        example_simple_search()
    elif example == "Búsqueda Avanzada":
        example_advanced_search()
    elif example == "Workflow Completo":
        example_complete_workflow()
