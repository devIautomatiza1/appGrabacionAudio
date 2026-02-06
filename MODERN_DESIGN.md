# 🎨 GUÍA DE IMPLEMENTACIÓN: DISEÑO MODERNO

**Fecha:** 2026-02-06  
**Versión:** 1.0  
**Status:** Listo para implementación

---

## 📋 TABLA DE CONTENIDOS

1. [Vista Previa del Diseño](#vista-previa-del-diseño)
2. [Instalación Rápida](#instalación-rápida)
3. [Integración en index.py](#integración-en-indexpy)
4. [Componentes Disponibles](#componentes-disponibles)
5. [Ejemplos de Uso](#ejemplos-de-uso)
6. [Resolución de Problemas](#resolución-de-problemas)

---

## 🎨 VISTA PREVIA DEL DISEÑO

### Paleta de Colores

```
🎯 COLORES PRINCIPALES:

Fondos:
├── Deep Navy (#0A0E27) - Fondo principal
├── Navy (#141829) - Fondo secundario
└── Dark Navy (#1A1F3A) - Tarjetas

Acentos:
├── Cian Eléctrico (#00FBFF) - Elementos principales
├── Violeta Neón (#8A2BE2) - Elementos IA
└── Azul Claro (#00D9FF) - Variante cian

Estados por Prioridad:
├── 🔴 High → Rojo Neón (#FF3B5C)
├── 🟡 Medium → Amarillo Neón (#FFB700)
└── 🟢 Low → Verde Neón (#00CC88)

Estados de Tickets:
├── New → Cian (#00FBFF)
├── In Progress → Amarillo (#FFB700)
├── Closed → Verde (#00CC88)
└── Won → Violeta (#8A2BE2)
```

### Características de Diseño

✨ **Glassmorphism**
- Fondos semitransparentes con blur
- Efecto de cristal congelado
- Profundidad visual sin cargar visualmente

🌟 **Efectos Glow**
- Botones principales con resplandor dinámico
- Cambios de color al hover
- Animaciones suaves

📐 **Tipografía**
- Fuentes: Inter (body), Inter Tight (headings)
- Espaciado generoso
- Excelente legibilidad

🎭 **Microinteracciones**
- Transiciones suaves (0.3s)
- Transformaciones en hover
- Efectos de profundidad

---

## 🚀 INSTALACIÓN RÁPIDA

### Paso 1: Copiar Archivo

Ya está en: `modern_ui.py`

### Paso 2: Importar en index.py

Una sóla línea al inicio de `index.py`:

```python
from modern_ui import inject_modern_css, section_header, stat_card, opportunity_card_modern, glow_button
```

### Paso 3: Inyectar CSS

**MUY IMPORTANTE:** Como primera línea de código (después de imports) en `index.py`:

```python
import streamlit as st
from modern_ui import inject_modern_css

# ⚠️ ESTO DEBE SER LO PRIMERO
inject_modern_css()

# Resto del código...
st.set_page_config(page_title="...", layout="wide")
```

### Paso 4: ¡Listo!

Tu aplicación ahora tendrá diseño moderno automáticamente.

---

## 📱 INTEGRACIÓN EN index.py

### Ejemplo de Integración Completa

```python
# archivo: index.py

import streamlit as st
import os
import AudioRecorder
import Transcriber
import Model
import OpportunitiesManager
from datetime import datetime
import hashlib
import database as db_utils

# 🎨 DISEÑO MODERNO - IMPORTAR Y APLICAR
from modern_ui import (
    inject_modern_css,
    section_header,
    stat_card,
    opportunity_card_modern,
    glow_button,
    badge,
    audio_player_modern,
    gradient_text,
    card_container
)

# ✅ INYECTAR CSS MODERNO (PRIMERO)
inject_modern_css()

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

st.set_page_config(
    page_title="🎙️ AudioPro Intelligence",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# INTERFAZ MEJORADA
# ============================================================================

# Encabezado con estilo
st.markdown("""
<div style="text-align: center; margin: 2rem 0; padding: 2rem;">
    <h1 style="font-size: 3rem; margin: 0;">🎙️ AudioPro</h1>
    <p style="color: #B0B8C1; font-size: 1.1rem; margin-top: 0.5rem;">
        Plataforma de IA para Transcripción y Análisis de Audios
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ============================================================================
# SECCIÓN 1: GRABACIÓN/CARGA DE AUDIOS
# ============================================================================

section_header("🎵 Grabación & Carga de Audios", "Sube o graba nuevos audios para analizar")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Opción 1: Grabar desde Micrófono**")
    # Tu código existente de grabación aquí
    pass

with col2:
    st.markdown("**Opción 2: Cargar Archivo**")
    # Tu código existente de carga aquí
    pass

st.divider()

# ============================================================================
# SECCIÓN 2: LISTADO DE AUDIOS
# ============================================================================

section_header("📂 Audios Disponibles", "Selecciona un audio para analizar")

recordings = db_utils.get_all_recordings()

if recordings:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        stat_card("Total Grabaciones", str(len(recordings)), "🎵", "cyan")
    with col2:
        stat_card("Procesadas", str(len([r for r in recordings if r.get('transcription')])), "✅", "low")
    with col3:
        stat_card("Pendientes", str(len([r for r in recordings if not r.get('transcription')])), "⏳", "medium")
    with col4:
        stat_card("Oportunidades", "Próxima actualización", "📋", "purple")
    
    st.divider()
    
    # Selectbox mejorado
    st.markdown("**Selecciona un audio para ver detalles:**")
    selected_audio = st.selectbox(
        "Audio",
        [r['filename'] for r in recordings],
        label_visibility="collapsed"
    )
    
    if selected_audio:
        st.markdown(f"**📁 {selected_audio}**")
        
        # Audio player moderno
        audio_player_modern(
            file_path=f"path/to/{selected_audio}",
            file_name=selected_audio
        )
else:
    st.info("📭 No hay audios disponibles. Carga uno para comenzar.")

st.divider()

# ============================================================================
# SECCIÓN 3: TRANSCRIPCIÓN
# ============================================================================

section_header("📝 Transcripción", "Convierte audio a texto automáticamente")

col1, col2 = st.columns([2, 1])

with col1:
    if st.session_state.get("contexto"):
        st.text_area(
            "Transcripción:",
            value=st.session_state.contexto,
            height=150,
            disabled=True,
            label_visibility="collapsed"
        )
    else:
        st.info("📭 No hay transcripción cargada")

with col2:
    st.write("")
    st.write("")
    
    # Botón con efecto glow
    if st.button(
        "🎙️ Transcribir",
        use_container_width=True,
        key="transcribe_btn",
        help="Usar IA para transcribir el audio"
    ):
        st.info("⏳ Transcribiendo...")
        # Tu código de transcripción aquí

st.divider()

# ============================================================================
# SECCIÓN 4: PALABRAS CLAVE
# ============================================================================

section_header("🔑 Palabras Clave", "Define palabras clave para buscar oportunidades")

col1, col2 = st.columns([2, 1])

with col1:
    keyword = st.text_input(
        "Nueva palabra clave:",
        placeholder="Ej: presupuesto, reunión, contrato...",
        label_visibility="collapsed"
    )
    
    if keyword and st.session_state.get("keywords") is not None:
        # Mostrar palabras clave existentes
        st.write("**Palabras clave agregadas:**")
        for kw in st.session_state.keywords.keys():
            badge(kw, "info")

with col2:
    st.write("")
    st.write("")
    
    if st.button(
        "➕ Agregar",
        use_container_width=True,
        key="add_keyword"
    ):
        if keyword:
            # Tu código aquí
            st.success(f"✅ '{keyword}' agregada")

st.divider()

# ============================================================================
# SECCIÓN 5: OPORTUNIDADES
# ============================================================================

section_header("🎯 Oportunidades Generadas", "Tickets creados automáticamente")

if st.button("🔄 Generar Oportunidades", use_container_width=False):
    with st.spinner("Analizando transcripción..."):
        # Tu código de generación aquí
        pass

st.divider()

# Mostrar oportunidades con tarjetas mejoradas
opportunities = []  # Reemplazar con tus datos reales

if opportunities:
    for opp in opportunities:
        opportunity_card_modern(
            ticket_number=opp.get('ticket_number', 0),
            title=opp.get('title', 'Sin título'),
            description=opp.get('description', 'Sin descripción'),
            status=opp.get('status', 'new'),
            priority=opp.get('priority', 'Medium'),
            notes=opp.get('notes', ''),
            created_at=opp.get('created_at', 'N/A')
        )
else:
    st.info("📭 No hay oportunidades. Genera algunas para comenzar.")

st.divider()

# ============================================================================
# SECCIÓN 6: CHAT CON IA
# ============================================================================

section_header("💬 Chat con IA", "Realiza preguntas sobre tu audio")

if st.session_state.get("chat_enabled"):
    # Tu código de chat aquí
    pass
else:
    st.info("💡 Carga un audio y genera oportunidades para habilitar el chat")

st.divider()

# ============================================================================
# SECCIÓN 7: DEBUG/MONITOR
# ============================================================================

section_header("🔍 Monitor de Sistema", "Estado de la aplicación")

with st.expander("📊 Ver Estadísticas", expanded=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        stat_card("Grabaciones", 
                 str(len(recordings) if recordings else 0), 
                 "🎵", "cyan")
    
    with col2:
        # Calcular oportunidades totales
        all_opps = db_utils.get_all_opportunities()
        stat_card("Oportunidades", 
                 str(len(all_opps) if all_opps else 0), 
                 "📋", "purple")
    
    with col3:
        # Calcular transcripciones
        all_trans = db_utils.get_all_transcriptions()
        stat_card("Transcripciones", 
                 str(len(all_trans) if all_trans else 0), 
                 "📝", "low")
```

---

## 🧩 COMPONENTES DISPONIBLES

### 1. **inject_modern_css()**

Inyecta todo el CSS personalizado. **DEBE SER LLAMADO PRIMERO.**

```python
from modern_ui import inject_modern_css

inject_modern_css()  # Punto 1 de tu código
```

---

### 2. **section_header(title, subtitle="")**

Encabezado de sección con estilo.

```python
from modern_ui import section_header

section_header("🎵 Grabaciones", "Sube o graba nuevos audios")
```

**Resultado:**
- Título en Cian
- Línea divisoria
- Subtítulo en gris

---

### 3. **stat_card(label, value, icon, color)**

Tarjeta para mostrar estadísticas con efecto glassmorphism.

```python
from modern_ui import stat_card

stat_card("Total Audios", "42", "🎵", "cyan")
stat_card("Prioridad Alta", "5", "🔴", "high")
```

**Colores disponibles:** `cyan`, `purple`, `high`, `medium`, `low`

---

### 4. **opportunity_card_modern(...)**

Tarjeta moderna para mostrar oportunidades con borde de color según prioridad.

```python
from modern_ui import opportunity_card_modern

opportunity_card_modern(
    ticket_number=1,
    title="Presupuesto",
    description="Cliente solicita presupuesto para proyecto...",
    status="new",  # 'new', 'in_progress', 'closed', 'won'
    priority="High",  # 'High', 'Medium', 'Low'
    notes="Cliente VIP - Seguimiento urgente",
    created_at="2026-02-06 14:30"
)
```

**Características:**
- Borde izquierdo coloreado según prioridad
- Efecto hover con glow
- Badges para estado y prioridad
- Sección de notas destacada

---

### 5. **badge(text, badge_type)**

Etiqueta/badge con estilo.

```python
from modern_ui import badge

badge("new", "status-new")
badge("High", "priority-high")
badge("In Progress", "status-progress")
```

**Tipos disponibles:**
```
Status: status-new, status-progress, status-closed, status-won
Priority: priority-high, priority-medium, priority-low
```

---

### 6. **glow_button(label, key, on_click, args)**

Botón con efecto glow para acciones principales.

```python
from modern_ui import glow_button

if glow_button("🎙️ Transcribir", key="transcribe"):
    # Tu código aquí
    pass
```

---

### 7. **audio_player_modern(file_path, file_name)**

Reproductor de audio con estilo glassmorphism.

```python
from modern_ui import audio_player_modern

audio_player_modern(
    file_path="path/to/audio.wav",
    file_name="Llamada_Cliente_2026-02-06.wav"
)
```

---

### 8. **card_container(content, priority)**

Contenedor genérico glassmorphism con borde de color.

```python
from modern_ui import card_container

card_container(
    content="<h3>Mi contenido</h3><p>Algo de texto</p>",
    priority="High"
)
```

---

### 9. **gradient_text(text, colors)**

Texto con gradiente de colores.

```python
from modern_ui import gradient_text

st.markdown("## ")
gradient_text("Tu texto con gradiente", 
             ["#00FBFF", "#8A2BE2"])
```

---

### 10. **loading_spinner(text)**

Spinner de carga con efecto glow.

```python
from modern_ui import loading_spinner

loading_spinner("Transcribiendo...")
```

---

### 11. **create_metric_row(metrics, cols)**

Crea una fila de tarjetas de métricas automáticamente.

```python
from modern_ui import create_metric_row

create_metric_row({
    "Grabaciones": "42",
    "Oportunidades": "128",
    "En Progreso": "15",
    "Completadas": "113"
}, cols=4)
```

---

## 💡 EJEMPLOS DE USO

### Ejemplo 1: Sección Completa de Audios

```python
from modern_ui import (
    inject_modern_css,
    section_header,
    stat_card,
    audio_player_modern,
    create_metric_row
)

inject_modern_css()

section_header("🎵 Mis Grabaciones", "Gestor de audios")

# Métricas
create_metric_row({
    "Total": "42",
    "Procesados": "38",
    "Pendientes": "4"
}, cols=3)

st.divider()

# Audio individual
audio_player_modern(
    file_path="path/to/audio.wav",
    file_name="meeting_2026-02-06.wav"
)
```

---

### Ejemplo 2: Lista de Oportunidades

```python
from modern_ui import (
    section_header,
    opportunity_card_modern,
    stat_card
)

section_header("🎯 Mis Oportunidades")

col1, col2, col3 = st.columns(3)

with col1:
    stat_card("Total", "47", "📋", "cyan")
with col2:
    stat_card("Nuevas", "8", "🆕", "medium")
with col3:
    stat_card("Ganadas", "39", "🏆", "low")

st.divider()

# Renderizar tarjetas
opportunities = [
    {
        "ticket_number": 1,
        "title": "Presupuesto",
        "description": "Cliente requiere presupuesto acotado...",
        "status": "new",
        "priority": "High",
        "notes": "VIP - responda hoy",
        "created_at": "2026-02-06 14:30"
    },
    # ... más oportunidades
]

for opp in opportunities:
    opportunity_card_modern(
        ticket_number=opp["ticket_number"],
        title=opp["title"],
        description=opp["description"],
        status=opp["status"],
        priority=opp["priority"],
        notes=opp["notes"],
        created_at=opp["created_at"]
    )
```

---

### Ejemplo 3: Dashboard Completo

```python
from modern_ui import *

inject_modern_css()

# Encabezado
st.markdown("<h1 style='text-align: center;'>📊 Dashboard Analytics</h1>", 
           unsafe_allow_html=True)

st.divider()

# Fila de métricas
create_metric_row({
    "Audios": "42",
    "Tickets": "128",
    "Resueltos": "113",
    "Ganadas": "89"
})

st.divider()

# Sección de oportunidades
section_header("Últimas Oportunidades", "Generadas en los últimos 7 días")

col1, col2 = st.columns([2, 1])

with col1:
    # Tus tarjetas aquí
    pass

with col2:
    st.subheader("Filtros")
    
    status = st.multiselect("Estado", ["new", "in_progress", "closed", "won"])
    priority = st.multiselect("Prioridad", ["High", "Medium", "Low"])
```

---

## 🔧 RESOLUCIÓN DE PROBLEMAS

### Problema 1: Los estilos no se aplicaron

**Solución:**
```python
# ❌ INCORRECTO
st.set_page_config(...)
inject_modern_css()  # Demasiado tarde

# ✅ CORRECTO
inject_modern_css()  # Primero
st.set_page_config(...)
```

---

### Problema 2: Los botones se ven normales (sin glow)

**Solución:** Los botones de Streamlit tienen estilos limitados. Para mejor control, usa HTML/CSS directo:

```python
st.markdown("""
<button style="
    background: linear-gradient(135deg, #00FBFF 0%, #00D9FF 100%);
    color: #0A0E27;
    border: none;
    padding: 12px 28px;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 0 20px rgba(0, 251, 255, 0.3);
" onclick="alert('Clickeado')">
    Click Me
</button>
""", unsafe_allow_html=True)
```

---

### Problema 3: Los colores no coinciden con la paleta

**Solución:** Los colores están definidos en el diccionario `COLORS` de `modern_ui.py`. Puedes personalizar:

```python
# En modern_ui.py
COLORS = {
    "bg_primary": "#0A0E27",      # Cambiar tu color aquí
    # ...
}
```

---

### Problema 4: Glassmorphism no aparece

**Asegúrate de:**
1. inject_modern_css() fue llamado
2. Usas los componentes correctos (stat_card, opportunity_card_modern, etc)
3. No sobrescribes los estilos con CSS propio

---

### Problema 5: El diseño no responde bien en móvil

**Ya está incluido:** El CSS tiene media queries para:
- Tablets (768px)
- Móviles (480px)

Si necesitas ajustes, edita en `modern_ui.py`:

```python
@media (max-width: 768px) {
    /* Los estilos responsivos van aquí */
}
```

---

## 📦 CHECKLIST DE IMPLEMENTACIÓN

```
✅ Copiar modern_ui.py al proyecto
✅ Importar inject_modern_css en index.py
✅ Llamar inject_modern_css() before st.set_page_config()
✅ Reemplazar section headers con section_header()
✅ Reemplazar stat cards con stat_card()
✅ Renderizar opportunities con opportunity_card_modern()
✅ Audios con audio_player_modern()
✅ Verificar que los colores se ven bien
✅ Probar en el navegador (Chrome/Firefox)
✅ Verificar en móvil
✅ Commit a GitHub
```

---

## 🎨 PERSONALIZACIÓN AVANZADA

### Cambiar Tema Completo

En `modern_ui.py`, modificar `COLORS`:

```python
COLORS = {
    "bg_primary": "#0A0E27",        # Cambiar fondo
    "accent_cyan": "#FF6B6B",       # Cambiar acento principal
    "accent_purple": "#4ECDC4",     # Cambiar acento secundario
    # ... etc
}
```

**Herramientas útiles:**
- Color picker: https://colorpicker.com
- Palette generator: https://www.colormind.io
- Contrast checker: https://webaim.org/resources/contrastchecker/

---

### Agregar Nuevo Componente

```python
# En modern_ui.py, al final

def mi_componente_personalizado(texto):
    """Mi nuevo componente"""
    html = f"""
    <div style="
        background: {COLORS['bg_tertiary']};
        border-radius: 12px;
        padding: 16px;
        color: {COLORS['text_primary']};
    ">
        {texto}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# En index.py
from modern_ui import mi_componente_personalizado

mi_componente_personalizado("Mi texto personalizado")
```

---

## 📚 RECURSOS

- **Icons:** https://unicode.org/emoji/
- **Fonts:** https://fonts.google.com (Inter/Inter Tight)
- **Colors:** https://chir.ag/projects/ntop/ (Color hex converter)
- **CSS Gradients:** https://www.cssgradient.io
- **Streamlit Docs:** https://docs.streamlit.io

---

## 🎉 ¡Listo!

Tu aplicación ahora tiene un diseño moderno, profesional e innovador.

**Próximos pasos:**
1. Implementar autenticación (desde MEJORAS_RECOMENDADAS.md)
2. Agregar dashboard analítico
3. Implementar búsqueda y filtrado
4. Exportar a Excel/PDF

---

**Última actualización:** 2026-02-06  
**Autor:** UI/UX Design Assistant  
**Versión CSS:** 1.0.0 Modern Edition
