# 🚀 MEJORAS RECOMENDADAS PARA EL PROYECTO

**Documento generado:** 2026-02-06  
**Proyecto:** Audio Recorder & Opportunity Manager  
**Estado actual:** Versión 1.0 Stable (Features Core Completas)

---

## 📋 TABLA DE CONTENIDOS

1. [Mejoras Críticas (Seguridad)](#mejoras-críticas-seguridad)
2. [Mejoras Importantes (Experiencia Usuario)](#mejoras-importantes-experiencia-usuario)
3. [Mejoras Recomendables (Escalabilidad)](#mejoras-recomendables-escalabilidad)
4. [Mejoras Nice to Have (UX)](#mejoras-nice-to-have-ux)
5. [Plan de Implementación Sugerido](#plan-de-implementación-sugerido)
6. [Priorización Final](#priorización-final)

---

## 🔴 MEJORAS CRÍTICAS (SEGURIDAD)

### 1. **Autenticación de Usuarios**

**Problema Actual:**
```
❌ Cualquiera con acceso a la URL puede ver todos los audios y tickets
❌ No hay concepto de "usuarios" - todo es compartido
❌ No se puede saber quién hizo qué cambio
```

**Solución Recomendada:** Supabase Auth

```python
# Implementación básica en index.py

import streamlit as st
from supabase import create_client, Client

# 1. Detectar usuario actual
user = st.session_state.get("user")
if not user:
    st.switch_page("pages/login.py")
    st.stop()

# 2. Todo filtrado por usuario_id
opportunities = supabase.table("opportunities") \
    .select("*") \
    .eq("user_id", user["id"]) \
    .execute()
```

**Beneficios:**
- ✅ Multi-usuario seguro
- ✅ Cada usuario ve solo sus datos
- ✅ Auditoría (quién hizo qué)
- ✅ Requerimiento para producción

**Esfuerzo:** ⭐⭐⭐ (3-5 días)  
**Impacto:** 🔴 CRÍTICO

**Pasos:**
1. Habilitar Auth en Supabase (Google, GitHub, Email)
2. Crear página de login (`pages/login.py`)
3. Agregar `user_id` a todas las tablas
4. Implementar RLS con `auth.uid()`

---

### 2. **Row Level Security (RLS) en Supabase**

**Problema Actual:**
```sql
-- ❌ VULNERABLE
CREATE POLICY "Public Access Opportunities" 
    ON public.opportunities 
    FOR ALL USING (true);  -- ¡Acceso total a todos!
```

**Solución:**

```sql
-- ✅ SEGURO
-- Primero, agregar user_id a las tablas

ALTER TABLE public.recordings 
ADD COLUMN user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE;

ALTER TABLE public.opportunities 
ADD COLUMN user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE;

ALTER TABLE public.transcriptions 
ADD COLUMN user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE;

-- Luego, crear políticas por usuario

-- Recordings: Solo el propietario puede ver/editar
CREATE POLICY "Users can view own recordings" 
    ON public.recordings 
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own recordings" 
    ON public.recordings 
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own recordings" 
    ON public.recordings 
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own recordings" 
    ON public.recordings 
    FOR DELETE USING (auth.uid() = user_id);

-- Lo mismo para opportunities y transcriptions
```

**Esfuerzo:** ⭐⭐ (2-3 días)  
**Impacto:** 🔴 CRÍTICO

---

### 3. **Validación y Sanitización de Inputs**

**Problema Actual:**
```python
# ❌ Sin validación
title = st.text_input("Título")
notes = st.text_area("Notas")
# Usuario puede:
# - Poner strings vacíos
# - Strings de 10,000 caracteres
# - Caracteres especiales que quiebren SQL
```

**Solución con Pydantic:**

```python
# archivo: validators.py

from pydantic import BaseModel, Field, validator
from typing import Literal

class OpportunityValidator(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=1000)
    notes: str = Field("", max_length=500)
    status: Literal["new", "in_progress", "closed", "won"]
    priority: Literal["Low", "Medium", "High"]
    
    @validator('title')
    def title_alphanumeric(cls, v):
        if not v.replace(" ", "").isalnum():
            raise ValueError('Título solo puede contener letras y números')
        return v.strip()

class AudioUploadValidator(BaseModel):
    filename: str = Field(..., max_length=255)
    max_file_size_mb: int = 100  # Límite 100MB
    
    @validator('filename')
    def filename_valid(cls, v):
        allowed_extensions = {'.wav', '.mp3', '.m4a', '.webm', '.ogg', '.flac'}
        if not any(v.lower().endswith(ext) for ext in allowed_extensions):
            raise ValueError(f'Formato no soportado. Permitidos: {allowed_extensions}')
        return v
```

**En index.py:**

```python
from validators import OpportunityValidator

# Cuando usuario intenta guardar
try:
    validated_opp = OpportunityValidator(
        title=st.session_state.title,
        description=context,
        notes=st.session_state.notes,
        status=st.session_state.status,
        priority=st.session_state.priority
    )
    # Guardar en Supabase
    save_opportunity(validated_opp.dict())
    st.success("✅ Ticket guardado")
except ValueError as e:
    st.error(f"❌ Error: {e}")
```

**Esfuerzo:** ⭐⭐ (2 días)  
**Impacto:** 🔴 ALTO

---

### 4. **Manejo Robusto de Errores**

**Problema Actual:**
```python
# ❌ Si Supabase falla, la app se quiebra
result = supabase.table("opportunities").select("*").execute()
# Si no hay conexión → RuntimeError sin mensaje útil
```

**Solución:**

```python
# archivo: error_handler.py

import streamlit as st
import logging
from typing import Optional, Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 2  # segundos

def safe_supabase_call(
    func, 
    *args, 
    fallback_value: Optional[Any] = None,
    error_message: str = "Error en la operación"
):
    """
    Ejecuta llamada a Supabase con reintentos exponenciales
    """
    import time
    
    for attempt in range(MAX_RETRIES):
        try:
            return func(*args)
        except Exception as e:
            logger.error(f"Intento {attempt + 1}/{MAX_RETRIES}: {str(e)}")
            
            if attempt == MAX_RETRIES - 1:  # Último intento
                st.error(f"❌ {error_message}. Por favor intenta más tarde.")
                logger.critical(f"Operación fallida después de {MAX_RETRIES} intentos", 
                              exc_info=True)
                return fallback_value
            
            time.sleep(RETRY_DELAY ** attempt)  # Espera exponencial

# Uso en base de datos
def get_opportunities_safe(recording_id):
    return safe_supabase_call(
        lambda: OpportunitiesManager().load_opportunities(recording_id),
        fallback_value=[],
        error_message="No se pudieron cargar los tickets"
    )
```

**En index.py:**

```python
from error_handler import safe_supabase_call

opportunities = safe_supabase_call(
    OpportunitiesManager().load_opportunities,
    selected_audio,
    fallback_value=[],
    error_message="No se pudieron cargar los tickets"
)
```

**Esfuerzo:** ⭐⭐ (2 días)  
**Impacto:** 🔴 ALTO

---

### 5. **Sistema de Auditoría (Audit Trail)**

**Problema Actual:**
```
❌ No hay registro de quién cambió qué y cuándo
❌ No cumple con GDPR/compliance
❌ No puedes deshacer cambios accidentales
```

**Solución:**

```sql
-- Crear tabla de auditoría

CREATE TABLE public.audit_logs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL REFERENCES auth.users(id),
    action text NOT NULL, -- 'created', 'updated', 'deleted'
    table_name text NOT NULL,
    record_id uuid,
    changes jsonb, -- {before: {...}, after: {...}}
    ip_address text,
    user_agent text,
    created_at timestamp with time zone DEFAULT now()
);

CREATE INDEX idx_audit_logs_user_id ON public.audit_logs(user_id);
CREATE INDEX idx_audit_logs_table_name ON public.audit_logs(table_name);
CREATE INDEX idx_audit_logs_created_at ON public.audit_logs(created_at);
```

**En Python (database.py):**

```python
def log_audit(user_id, action, table_name, record_id, changes=None):
    """Registra cambio en tabla de auditoría"""
    try:
        supabase.table("audit_logs").insert({
            "user_id": user_id,
            "action": action,  # 'created'/'updated'/'deleted'
            "table_name": table_name,
            "record_id": record_id,
            "changes": changes or {},
            "ip_address": get_user_ip(),
            "user_agent": st.session_state.get("user_agent")
        }).execute()
    except Exception as e:
        logger.error(f"Error en audit log: {e}")

# Uso al actualizar un ticket
def update_opportunity(opp_id, new_values):
    old_values = get_opportunity_by_id(opp_id)
    result = db.update_opportunity(opp_id, new_values)
    
    log_audit(
        user_id=st.session_state.user["id"],
        action="updated",
        table_name="opportunities",
        record_id=opp_id,
        changes={"before": old_values, "after": new_values}
    )
    return result
```

**Esfuerzo:** ⭐⭐⭐ (3 días)  
**Impacto:** 🔴 CRÍTICO (para compliance)

---

## 🟡 MEJORAS IMPORTANTES (EXPERIENCIA USUARIO)

### 6. **Búsqueda y Filtrado de Tickets**

**Problema Actual:**
```
❌ Solo ves los tickets del audio actual
❌ No puedes buscar un ticket específico
❌ No puedes filtrar por estado/prioridad
```

**Solución:**

```python
# En index.py - nueva sección

st.header("🔍 Buscar & Filtrar Tickets")

col1, col2, col3, col4 = st.columns(4)

with col1:
    search_query = st.text_input("🔍 Buscar por keyword/descripción")

with col2:
    status_filter = st.multiselect(
        "Estado",
        ["new", "in_progress", "closed", "won"],
        default=["new", "in_progress"]
    )

with col3:
    priority_filter = st.multiselect(
        "Prioridad",
        ["Low", "Medium", "High"],
        default=["High", "Medium"]
    )

with col4:
    date_range = st.date_input("Rango de fechas", value=(None, None))

# Filtrar y mostrar
filtered_opportunities = filter_opportunities(
    search_query=search_query,
    status=status_filter,
    priority=priority_filter,
    date_range=date_range
)

st.write(f"📊 Mostrando {len(filtered_opportunities)} de {len(all_opportunities)} tickets")

# Mostrar tabla
df = pd.DataFrame(filtered_opportunities)
st.dataframe(
    df[['title', 'status', 'priority', 'created_at', 'notes']],
    use_container_width=True
)
```

**En database.py:**

```python
def filter_opportunities(
    search_query: str = "",
    status: List[str] = None,
    priority: List[str] = None,
    date_range: tuple = None,
    user_id: str = None
):
    """Filtro completo de tickets"""
    query = supabase.table("opportunities").select("*")
    
    if user_id:
        query = query.eq("user_id", user_id)
    
    if status:
        query = query.in_("status", status)
    
    if priority:
        query = query.in_("priority", priority)
    
    if search_query:
        query = query.or_(
            f"title.ilike.%{search_query}%,"
            f"description.ilike.%{search_query}%"
        )
    
    if date_range[0] and date_range[1]:
        query = query.gte("created_at", date_range[0].isoformat()) \
                   .lte("created_at", date_range[1].isoformat())
    
    result = query.order("priority", desc=True) \
                  .order("created_at", desc=True) \
                  .execute()
    
    return result.data or []
```

**Esfuerzo:** ⭐⭐ (2 días)  
**Impacto:** 🟡 ALTO

---

### 7. **Exportar Datos (Excel/PDF)**

**Problema Actual:**
```
❌ No puedes extraer datos en formato reutilizable
❌ No hay forma de compartir reportes
```

**Solución:**

```bash
pip install openpyxl reportlab python-dateutil
```

```python
# archivo: export_utils.py

import pandas as pd
from datetime import datetime
from io import BytesIO

def export_to_excel(opportunities_list):
    """Exporta tickets a Excel"""
    df = pd.DataFrame(opportunities_list)
    
    # Renombrar columnas
    df.columns = ['ID', 'Título', 'Descripción', 'Estado', 'Prioridad', 'Notas', 'Creado']
    
    # Formatear fechas
    df['Creado'] = pd.to_datetime(df['Creado']).dt.strftime('%Y-%m-%d %H:%M')
    
    # Generar archivo en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Tickets', index=False)
        
        # Formatear
        worksheet = writer.sheets['Tickets']
        for column in worksheet.columns:
            max_length = max(len(str(cell.value)) for cell in column)
            worksheet.column_dimensions[column[0].column_letter].width = max_length + 2
    
    return output.getvalue()

def export_to_pdf(opportunities_list):
    """Exporta tickets a PDF"""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.units import inch
    
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    
    # Crear tabla
    data = [['Título', 'Estado', 'Prioridad', 'Notas']]
    for opp in opportunities_list:
        data.append([
            opp['title'],
            opp['status'],
            opp['priority'],
            opp['notes'][:50] + '...' if len(opp['notes']) > 50 else opp['notes']
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), (0.2, 0.2, 0.2)),
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
    ]))
    
    doc.build([table])
    return output.getvalue()
```

**En index.py:**

```python
from export_utils import export_to_excel, export_to_pdf

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📥 Descargar Excel"):
        excel_data = export_to_excel(opportunities)
        st.download_button(
            label="Descargar Excel",
            data=excel_data,
            file_name=f"tickets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with col2:
    if st.button("📥 Descargar PDF"):
        pdf_data = export_to_pdf(opportunities)
        st.download_button(
            label="Descargar PDF",
            data=pdf_data,
            file_name=f"tickets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )

with col3:
    if st.button("📥 Descargar JSON"):
        json_data = json.dumps(opportunities, indent=2, default=str)
        st.download_button(
            label="Descargar JSON",
            data=json_data,
            file_name=f"tickets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
```

**Esfuerzo:** ⭐⭐ (2 días)  
**Impacto:** 🟡 MEDIO

---

### 8. **Dashboard/Analytics**

**Problema Actual:**
```
❌ No hay visibilidad del estado general
❌ No sabes qué palabras clave son más efectivas
❌ No sabes velocidad de generación de tickets
```

**Solución:**

```python
# En index.py o nueva página: pages/dashboard.py

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="📊 Dashboard", layout="wide")

# Cargar datos
all_opportunities = load_all_opportunities()
all_recordings = load_all_recordings()

# Tarjetas de métricas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📊 Total Tickets",
        len(all_opportunities),
        delta=f"+{len([o for o in all_opportunities if is_today(o['created_at'])])} hoy"
    )

with col2:
    closed_count = len([o for o in all_opportunities if o['status'] == 'closed'])
    win_rate = (closed_count / len(all_opportunities) * 100) if all_opportunities else 0
    st.metric("✅ Tasa Resolución", f"{win_rate:.1f}%")

with col3:
    high_priority = len([o for o in all_opportunities if o['priority'] == 'High'])
    st.metric("🔴 Alta Prioridad", high_priority)

with col4:
    avg_days = calculate_avg_resolution_time(all_opportunities)
    st.metric("⏱️ Días Prom Cierre", f"{avg_days:.1f}")

# Gráficos
st.header("📈 Análisis")

col1, col2 = st.columns(2)

with col1:
    # Pie chart: Estado de tickets
    status_counts = pd.Series([o['status'] for o in all_opportunities]).value_counts()
    fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Distribución por Estado"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Bar chart: Prioridad
    priority_counts = pd.Series([o['priority'] for o in all_opportunities]).value_counts()
    fig = px.bar(
        x=priority_counts.index,
        y=priority_counts.values,
        title="Tickets por Prioridad",
        labels={'x': 'Prioridad', 'y': 'Cantidad'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Línea de tiempo: Tickets por día
col1, col2 = st.columns(2)

with col1:
    # Audios transcribidos por día (últimos 30 días)
    last_30 = datetime.now() - timedelta(days=30)
    recent = [r for r in all_recordings if parse_date(r['created_at']) > last_30]
    
    daily_counts = pd.Series([parse_date(r['created_at']).date() for r in recent]).value_counts().sort_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_counts.index,
        y=daily_counts.values,
        mode='lines+markers',
        name='Audios'
    ))
    fig.update_layout(title='Audios Procesados (Últimos 30 días)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Top 10 palabras clave
    keywords = {}
    for opp in all_opportunities:
        kw = opp.get('title', 'N/A')
        keywords[kw] = keywords.get(kw, 0) + 1
    
    top_10 = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10]
    
    fig = px.bar(
        x=[k[0] for k in top_10],
        y=[k[1] for k in top_10],
        title='Top 10 Palabras Clave',
        labels={'x': 'Palabra Clave', 'y': 'Ocurrencias'}
    )
    st.plotly_chart(fig, use_container_width=True)
```

**Agregue a requirements.txt:**
```
plotly>=5.0.0
pandas>=2.0.0
```

**Esfuerzo:** ⭐⭐⭐ (3 días)  
**Impacto:** 🟡 ALTO

---

### 9. **Procesamiento Batch de Múltiples Audios**

**Problema Actual:**
```
❌ Solo transcribes 1 audio a la vez
❌ No hay forma de procesar lotes
```

**Solución:**

```python
# En pages/batch_processing.py

import streamlit as st
import time

st.title("⚙️ Procesamiento en Lote")

# Seleccionar múltiples audios
st.header("1️⃣ Seleccionar Audios")

all_recordings = get_all_recordings()
unprocessed = [r for r in all_recordings if not r.get('transcription')]

selected_audios = st.multiselect(
    "Elige audios para procesar",
    [r['filename'] for r in unprocessed]
)

if selected_audios:
    st.write(f"✅ {len(selected_audios)} audios seleccionados")
    
    # Mostrar opciones de procesamiento
    st.header("2️⃣ Configurar Procesamiento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        api_choice = st.radio(
            "API de transcripción",
            ["Gemini (Gratis)", "OpenAI (Pago)"]
        )
    
    with col2:
        language = st.selectbox("Idioma", ["Español", "English", "Français"])
    
    # Botón iniciar
    if st.button("▶️ Iniciar Procesamiento", key="start_batch"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        results = st.container()
        
        for idx, audio_filename in enumerate(selected_audios):
            # Actualizar progreso
            progress = (idx + 1) / len(selected_audios)
            progress_bar.progress(progress)
            status_text.text(f"Procesando {idx + 1}/{len(selected_audios)}: {audio_filename}")
            
            try:
                # Transcribir
                transcription = transcribe_audio(audio_filename, api_choice)
                
                # Guardar
                save_transcription(audio_filename, transcription, language)
                
                # Mostrar resultado
                with results:
                    st.success(f"✅ {audio_filename}")
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                with results:
                    st.error(f"❌ {audio_filename}: {str(e)}")
        
        st.success("🎉 Procesamiento completado")
```

**Esfuerzo:** ⭐⭐⭐ (3 días)  
**Impacto:** 🟡 MEDIO

---

### 10. **Historial de Cambios en Tickets**

**Problema Actual:**
```
❌ No sabes quién cambió el estado
❌ No sabes cuándo se cambió
❌ No puedes revertir cambios accidentales
```

**Solución:**

```python
# En index.py - sección "Detalles del Ticket"

st.subheader(f"📝 Ticket #{opportunity['ticket_number']}")

# Información actual
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Estado", opportunity['status'])
with col2:
    st.metric("Prioridad", opportunity['priority'])
with col3:
    st.metric("Creado", format_date(opportunity['created_at']))

# Historial de cambios
st.subheader("📋 Historial de Cambios")

changes = get_audit_log(opportunity['id'], "opportunities")

if changes:
    for change in changes:
        with st.container():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.caption(format_date(change['created_at']))
            
            with col2:
                before = change['changes'].get('before', {})
                after = change['changes'].get('after', {})
                
                for field in ['status', 'priority', 'notes']:
                    if before.get(field) != after.get(field):
                        st.write(f"**{field.upper()}:** `{before.get(field)}` → `{after.get(field)}`")
                
                st.caption(f"Por: {change['user_email']}")
            
            st.divider()
else:
    st.info("Sin cambios registrados")
```

**Esfuerzo:** ⭐⭐ (2 días)  
**Impacto:** 🟡 MEDIO

---

## 🟢 MEJORAS RECOMENDABLES (ESCALABILIDAD)

### 11. **API REST con FastAPI**

**Descripción:** Permitir que sistemas externos se integren con tu app

```bash
pip install fastapi uvicorn
```

```python
# archivo: api.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="Audio Manager API", version="1.0.0")

# Autenticación con Bearer token
async def verify_token(token: str = Depends(oauth2_scheme)):
    user = get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# Endpoints

@app.post("/api/audio/upload")
async def upload_audio(file: UploadFile, user = Depends(verify_token)):
    """Subir nuevo audio"""
    pass

@app.get("/api/audio/{audio_id}")
async def get_audio(audio_id: str, user = Depends(verify_token)):
    """Obtener información de audio"""
    pass

@app.get("/api/opportunities")
async def list_opportunities(
    status: str = None,
    priority: str = None,
    limit: int = 100,
    user = Depends(verify_token)
):
    """Listar tickets con filtros"""
    pass

@app.put("/api/opportunities/{opp_id}")
async def update_opportunity(opp_id: str, data: OpportunityUpdate, user = Depends(verify_token)):
    """Actualizar ticket"""
    pass

@app.delete("/api/opportunities/{opp_id}")
async def delete_opportunity(opp_id: str, user = Depends(verify_token)):
    """Eliminar ticket"""
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Uso:** Integraciones con CRM, mobile apps, bots, etc.

**Esfuerzo:** ⭐⭐⭐⭐ (4-5 días)  
**Impacto:** 🟢 ALTO

---

### 12. **Webhooks**

**Descripción:** Notificar a sistemas externos cuando ocurren eventos

```python
# archivo: webhooks.py

import httpx
import json
from functools import wraps

WEBHOOKS = {
    "on_transcription_complete": [],
    "on_opportunity_created": [],
    "on_opportunity_status_changed": [],
}

def trigger_webhook(event_name: str, data: dict):
    """Dispara webhook para todos los listeners registrados"""
    for webhook_url in WEBHOOKS.get(event_name, []):
        try:
            httpx.post(
                webhook_url,
                json={
                    "event": event_name,
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=10
            )
        except Exception as e:
            logger.error(f"Webhook {webhook_url} failed: {e}")

# Uso en el código
def save_transcription_with_webhook(recording_filename, content, language="es"):
    result = save_transcription(recording_filename, content, language)
    
    trigger_webhook("on_transcription_complete", {
        "recording_filename": recording_filename,
        "transcription_id": result,
        "language": language
    })
    
    return result
```

**Configurar webhooks:** Panel de administración donde usuarios registren URLs

**Esfuerzo:** ⭐⭐⭐ (3 días)  
**Impacto:** 🟢 MEDIO

---

### 13. **Caché de Transcripciones**

**Descripción:** Reutilizar transcripción si el audio ya fue procesado

```python
# archivo: cache_manager.py

import hashlib
from datetime import datetime, timedelta

def get_audio_hash(file_path: str) -> str:
    """Genera hash MD5 del archivo de audio"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_cached_transcription(audio_hash: str):
    """Busca transcripción en caché"""
    cache = supabase.table("transcription_cache") \
        .select("*") \
        .eq("audio_hash", audio_hash) \
        .order("created_at", desc=True) \
        .limit(1) \
        .execute()
    
    if cache.data:
        return cache.data[0]['content']
    return None

def cache_transcription(audio_hash: str, content: str, language: str):
    """Guarda transcripción en caché"""
    supabase.table("transcription_cache").insert({
        "audio_hash": audio_hash,
        "content": content,
        "language": language,
        "created_at": datetime.now().isoformat()
    }).execute()

# Uso en Transcriber
def transcript_audio_with_cache(audio_path, language="es"):
    audio_hash = get_audio_hash(audio_path)
    
    # Intentar obtener del caché
    cached = get_cached_transcription(audio_hash)
    if cached:
        st.info("📦 Usando transcripción en caché (sin costo)")
        return cached
    
    # Si no está en caché, transcribir normalmente
    transcription = transcribe_audio_api(audio_path)
    
    # Guardar en caché
    cache_transcription(audio_hash, transcription, language)
    
    return transcription
```

**Beneficio:** Ahorrar ~80% en costos de API

**Esfuerzo:** ⭐⭐ (2 días)  
**Impacto:** 🟢 MEDIO

---

### 14. **Queue para Procesamiento en Background**

**Descripción:** Procesar trabajos pesados sin bloquear la UI

```bash
pip install celery redis
```

```python
# archivo: tasks.py

from celery import Celery

app = Celery('audio_processor')
app.conf.broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

@app.task(bind=True)
def transcribe_audio_task(self, audio_path: str, language: str = "es"):
    """Tarea de transcripción en background"""
    try:
        self.update_state(state='PROGRESS', meta={'current': 0, 'total': 100})
        
        transcription = transcribe_audio_api(audio_path)
        
        save_transcription(audio_path, transcription, language)
        
        # Notificar completación
        trigger_webhook("on_transcription_complete", {
            "audio_path": audio_path,
            "status": "success"
        })
        
        return {'status': 'success', 'transcription_id': '...'}
    
    except Exception as e:
        self.update_state(
            state='FAILURE',
            meta={'error': str(e)}
        )
        raise

# En index.py
if st.button("▶️ Transcribir en Background"):
    task = transcribe_audio_task.delay(selected_audio, "es")
    
    st.info(f"⏳ Procesando... Task ID: {task.id}")
    
    # Polling del estado
    with st.spinner("Transcribiendo..."):
        while True:
            state = task.state
            if state == 'PENDING':
                st.write("⏳ En cola...")
            elif state == 'PROGRESS':
                progress = task.info.get('current', 0) / task.info.get('total', 100)
                st.progress(progress)
            elif state == 'SUCCESS':
                st.success("✅ Completado")
                break
            elif state == 'FAILURE':
                st.error(f"❌ Error: {task.info.get('error')}")
                break
            
            time.sleep(1)
```

**Esfuerzo:** ⭐⭐⭐⭐ (4 días)  
**Impacto:** 🟢 ALTO

---

### 15. **CI/CD Pipeline con GitHub Actions**

**Descripción:** Automatizar tests, linting y deploy

```yaml
# .github/workflows/ci.yml

name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pylint black
    
    - name: Lint with pylint
      run: pylint **/*.py
    
    - name: Format check with black
      run: black --check .
    
    - name: Run tests
      run: pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Streamlit Cloud
      run: |
        curl -X POST https://api.streamlit.cloud/api/v1/deployments \
          -H "Authorization: Bearer ${{ secrets.STREAMLIT_API_TOKEN }}"
```

**Esfuerzo:** ⭐⭐⭐ (3 días)  
**Impacto:** 🟢 ALTO

---

## 🎨 MEJORAS NICE TO HAVE (UX)

| Feature | Descripción | Esfuerzo | Impacto |
|---------|-------------|----------|--------|
| **Temas oscuro/claro** | Selector de tema | ⭐ | 🟢 |
| **Soporte multiidioma** | ES/EN/FR/DE | ⭐⭐⭐ | 🔴 |
| **Traducción automática** | Traducir audios a otros idiomas | ⭐⭐ | 🟡 |
| **Análisis de sentimiento** | Detectar sentimiento en transcripciones | ⭐⭐ | 🟡 |
| **Grabación streaming** | No solo archivos, sino stream de micrófono | ⭐⭐⭐⭐ | 🔴 |
| **Edición de transcripciones** | Corregir errores manualmente | ⭐ | 🟢 |
| **Atajos de teclado** | Ctrl+N para nuevo ticket, etc | ⭐ | 🟢 |
| **Modo offline** | Funcionar sin conexión internet | ⭐⭐⭐⭐ | 🟡 |
| **Compartir tickets** | Link para compartir tickets con otros | ⭐⭐ | 🟡 |
| **Notificaciones desktop** | Avisar cuando ndo ticket creado | ⭐ | 🟢 |

---

## 📊 PLAN DE IMPLEMENTACIÓN SUGERIDO

### **FASE 1: SEGURIDAD (Semanas 1-2)**
**Prioridad: MÁXIMA - Esto es bloqueante para producción**

- [ ] Autenticación con Supabase Auth (Google/GitHub)
- [ ] Implementar RLS en todas las tablas
- [ ] Validación con Pydantic

**Motivo:** Sin esto no es seguro para multi-usuario

---

### **FASE 2: EXPERIENCIA USUARIO (Semanas 3-4)**
**Prioridad: ALTA - Mejora notablemente el flujo**

- [ ] Búsqueda y filtrado de tickets
- [ ] Exportar a Excel/PDF
- [ ] Dashboard básico con gráficos
- [ ] Historial de cambios

**Motivo:** Usuarios productivos esperan estas features

---

### **FASE 3: OPERACIONAL (Semanas 5-6)**
**Prioridad: MEDIA - Importante para escalabilidad**

- [ ] Sistema de auditoría (audit logs)
- [ ] Manejo robusto de errores
- [ ] Procesamiento batch
- [ ] Caché de transcripciones

**Motivo:** Necesario cuando usadores aumentan

---

### **FASE 4: INTEGRACIÓN (Semanas 7+)**
**Prioridad: BAJA - Para integraciones futuras**

- [ ] API REST
- [ ] Webhooks
- [ ] Queue con Celery
- [ ] CI/CD pipeline

**Motivo:** Cuando necesites conectar sistemas externos

---

## 🎯 PRIORIZACIÓN FINAL

### **🔴 HAGA PRIMERO (Crítico):**
1. **Autenticación** - Sin esto no es producción
2. **RLS** - Seguridad de datos
3. **Validación** - Evitar errores de usuario
4. **Auditoría** - Para compliance

**Tiempo:** 2-3 semanas

---

### **🟡 HAGA DESPUÉS (Importante):**
5. **Búsqueda/Filtrado** - UX esperada
6. **Exportación** - Usuarios lo piden
7. **Dashboard** - Visibilidad
8. **Manejo Errores** - Confiabilidad

**Tiempo:** 2-3 semanas

---

### **🟢 OPCIONAL (Escalabilidad):**
9. **API REST** - Integraciones
10. **Webhooks** - Automatización
11. **Caché** - Reducir costos
12. **CI/CD** - Deployment

**Tiempo:** 3-4 semanas

---

## 📋 CHECKLIST RÁPIDO

```
Seguridad:
☐ Autenticación de usuarios
☐ RLS en Supabase
☐ Validación de inputs
☐ Manejo robusto de errores
☐ Auditoría de cambios

Experiencia Usuario:
☐ Búsqueda y filtrado
☐ Exportar Excel/PDF
☐ Dashboard con gráficos
☐ Historial de cambios
☐ Procesamiento batch

Escalabilidad:
☐ API REST
☐ Webhooks
☐ Caché
☐ Queue de procesamiento
☐ CI/CD

Nice to Have:
☐ Tema oscuro/claro
☐ Multiidioma
☐ Traducción automática
☐ Análisis de sentimiento
☐ Modo offline
```

---

## 🤝 Recomendación Personal

**Si tienes 1 mes:** Haz **FASE 1 + FASE 2** (Seguridad + UX)  
**Si tienes 6 semanas:** Haz **TODO** hasta FASE 3  
**Si tienes tiempo ilimitado:** Implementa TODO incluyendo FASE 4

La app actual funciona bien como MVP, pero **NECESITA autenticación antes de cualquier uso en producción real**.

---

**Documento creado:** 2026-02-06  
**Autor:** AI Assistant  
**Próxima revisión recomendada:** 2026-03-06
