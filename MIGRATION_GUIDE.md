# 📖 Guía de Migración - Paso a Paso

## 🎯 Objetivo
Convertir llamadas directas a Supabase en el frontend (index.py) a llamadas de servicios en el backend.

## 📝 Equivalencias - Antes vs Después

### 1. Guardar Grabación

**ANTES (❌ Inseguro)**
```python
# En index.py - Acoplado
import database as db_utils

audio_data = st.audio_input("Graba aquí")
if audio_data:
    # Guardar localmente
    with open(f"recordings/{filename}", "wb") as f:
        f.write(audio_data.getbuffer())
    
    # Guardar en BD directamente
    recording_id = db_utils.save_recording_to_db(filename, filepath)
```

**DESPUÉS (✅ Seguro y Limpio)**
```python
# En index.py - Desacoplado
from backend.services import AudioService
from ui.notifications import show_success, show_error

audio_service = AudioService()

audio_data = st.audio_input("Graba aquí")
if audio_data:
    # Guardar localmente
    with open(f"recordings/{filename}", "wb") as f:
        f.write(audio_data.getbuffer())
    
    # Guardar en BD vía servicio
    recording_id = audio_service.save_recording(filename, filepath)
    
    if recording_id:
        show_success(f"Grabación guardada: {filename}")
    else:
        show_error("Error al guardar grabación")
```

### 2. Obtener Grabaciones

**ANTES (❌)**
```python
# En index.py
from database import get_all_recordings

recordings = get_all_recordings()
```

**DESPUÉS (✅)**
```python
# En index.py
from backend.services import AudioService

audio_service = AudioService()
recordings = audio_service.get_all_recordings()
```

### 3. Guardar Transcripción

**ANTES (❌)**
```python
# En index.py
from database import save_transcription

transcription_id = save_transcription(filename, transcription_content)
```

**DESPUÉS (✅)**
```python
# En index.py
from backend.services import TranscriptionService

trans_service = TranscriptionService()

# Primero obtener el recording_id por filename
from backend.services import AudioService
audio_service = AudioService()
recording = audio_service.get_recording_by_filename(filename)

if recording:
    trans_id = trans_service.save_transcription(
        recording_id=recording["id"],
        content=transcription_content,
        language="es"
    )
```

### 4. Guardar Oportunidades

**ANTES (❌)**
```python
# En index.py
from database import save_opportunity

success = save_opportunity(recording_id, title, description)
```

**DESPUÉS (✅)**
```python
# En index.py
from backend.services import OpportunityService

opp_service = OpportunityService()
opp_id = opp_service.create_opportunity(
    recording_id=recording_id,
    title=title,
    description=description
)

if opp_id:
    show_success(f"Oportunidad creada: {title}")
```

### 5. Eliminar Grabación (Cascada)

**ANTES (❌)**
```python
# En index.py
from database import delete_recording_from_db

success = delete_recording_from_db(recording_id)
if success:
    st.success("Eliminado")
```

**DESPUÉS (✅)**
```python
# En index.py
from backend.services import AudioService

audio_service = AudioService()
success = audio_service.delete_recording(recording_id)

if success:
    show_success("Grabación eliminada")
else:
    show_error("Error al eliminar")
```

## 🔧 Cambios en index.py - Sección por Sección

### Imports - Actualizar

```python
# ❌ ANTES
import database as db_utils
from database import init_supabase

# ✅ DESPUÉS
from backend.services import AudioService, TranscriptionService, OpportunityService
from ui.styles import get_styles
from ui.notifications import show_success, show_error, show_warning, show_info
```

### Inicialización de Servicios

```python
# Agregar esto después de crear la UI:
audio_service = AudioService()
trans_service = TranscriptionService()
opp_service = OpportunityService()
```

### Sección de Grabación en Vivo

**ANTES:**
```python
if audio_data:
    # ... guardar localmente ...
    
    recording_id = db_utils.save_recording_to_db(filename, filepath)
    if recording_id:
        st.session_state.recordings = recorder.get_recordings_from_supabase()
```

**DESPUÉS:**
```python
if audio_data:
    # ... guardar localmente ...
    
    recording_id = audio_service.save_recording(filename, filepath)
    if recording_id:
        show_success(f"Grabación guardada: {filename}")
        st.session_state.recordings = audio_service.get_all_recordings()
```

### Sección de Transcripción

**ANTES:**
```python
transcription_text = transcriber_model.transcript_audio(audio_path)
db_utils.save_transcription(filename, transcription_text)

recording = db_utils.get_all_recordings()
st.success("Transcripción guardada")
```

**DESPUÉS:**
```python
transcription_text = transcriber_model.transcript_audio(audio_path)

# Obtener el recording_id
recording_data = audio_service.get_recording_by_filename(filename)
if recording_data:
    trans_id = trans_service.save_transcription(
        recording_id=recording_data["id"],
        content=transcription_text,
        language="es"
    )
    if trans_id:
        show_success("Transcripción guardada")
```

### Sección de Oportunidades

**ANTES:**
```python
for keyword in keywords_list:
    # Extraer oportunidades localmente
    opps = opp_manager.extract_opportunities(transcription, [keyword])
    
    # Guardar en BD
    for opp in opps:
        db_utils.save_opportunity(recording_id, opp["title"], opp["description"])
```

**DESPUÉS:**
```python
recording_data = audio_service.get_recording_by_filename(filename)
if recording_data:
    # Usar el servicio para extraer y guardar automáticamente
    created_ids = opp_service.extract_opportunities_from_keywords(
        recording_id=recording_data["id"],
        transcription=transcription_text,
        keywords=keywords
    )
    
    if created_ids:
        show_success(f"{len(created_ids)} oportunidades identificadas")
```

### Sección de Eliminación

**ANTES:**
```python
if st.button("Eliminar"):
    success = db_utils.delete_recording_by_filename(filename)
    if success:
        st.success("Eliminado")
```

**DESPUÉS:**
```python
if st.button("Eliminar"):
    recording_data = audio_service.get_recording_by_filename(filename)
    if recording_data:
        success = audio_service.delete_recording(recording_data["id"])
        if success:
            show_success("Grabación eliminada")
        else:
            show_error("Error al eliminar")
```

## 📋 Checklist de Migración

- [ ] Crear estructura de carpetas backend/
- [ ] Copiar config.py, supabase_client.py, validators.py
- [ ] Copiar repositories.py, schemas.py
- [ ] Copiar audio_service.py, transcription_service.py, opportunity_service.py
- [ ] Actualizar imports en index.py
- [ ] Reemplazar db_utils.save_recording_to_db() con audio_service.save_recording()
- [ ] Reemplazar db_utils.get_all_recordings() con audio_service.get_all_recordings()
- [ ] Reemplazar db_utils.save_transcription() con trans_service.save_transcription()
- [ ] Reemplazar db_utils.save_opportunity() con opp_service.create_opportunity()
- [ ] Reemplazar db_utils.delete_recording_from_db() con audio_service.delete_recording()
- [ ] Actualizar .env con credenciales
- [ ] Probar flujo completo
- [ ] Verificar que las notificaciones funcionan
- [ ] Limpiar archivos database.py antiguos (mantener como backup)

## 🚀 Ejecución Paso a Paso

### Paso 1: Copiar Archivos
```bash
# Ya están creados, solo verifica que existen:
backend/
├── config.py
├── supabase_client.py
├── validators.py
├── database/
│   ├── repositories.py
│   └── schemas.py
└── services/
    ├── audio_service.py
    ├── transcription_service.py
    └── opportunity_service.py
```

### Paso 2: Actualizar index.py
```python
# En la parte superior, reemplazar:
import database as db_utils

# Por:
from backend.services import AudioService, TranscriptionService, OpportunityService
from ui.styles import get_styles
from ui.notifications import show_success, show_error, show_warning, show_info
```

### Paso 3: Inicializar Servicios
```python
# Después de inicializar los modelos:
audio_service = AudioService()
trans_service = TranscriptionService()
opp_service = OpportunityService()
```

### Paso 4: Reemplazar Llamadas
Buscar y reemplazar cada patrón según las equivalencias arriba.

### Paso 5: Probar
```bash
# Terminal
streamlit run index.py

# Verificar:
# 1. Grabar audio ✓
# 2. Transcribir ✓
# 3. Crear oportunidades ✓
# 4. Eliminar grabación ✓
# 5. Ver historial ✓
```

## 🐛 Troubleshooting

### Error: "No module named 'backend'"
**Solución**: Asegurar que estás en el directorio raíz del proyecto y que existe `backend/__init__.py`

### Error: "SUPABASE_URL not found"
**Solución**: Verificar que el archivo `.env` existe con las credenciales

### Error: "Recording with ID X not exists"
**Solución**: El servicio está validando que el recording existe antes de crear transcripciones/oportunidades

### Error: "No attribute X in service"
**Solución**: Verificar que estás usando el nombre correcto del método del servicio

## 📊 Comparación: Antes vs Después

| Métrica | Antes | Después |
|---------|-------|---------|
| Archivos que saben de Supabase | 5+ | 1 (supabase_client.py) |
| Lugares donde se validan datos | 0 (no hay) | 1 (validators.py) |
| Acoplamiento frontend-BD | Alto | Bajo (via servicios) |
| Credenciales hardcoded | Sí | No |
| Complejidad de index.py | Alta | Media |
| Testeable sin Streamlit | No | Sí |
| Reutilizable en otra UI / API | No | Sí |

---

**Nota**: Los archivos antiguos (database.py, OpportunitiesManager.py) se dejan como fallback pero NO deben ser usados.
