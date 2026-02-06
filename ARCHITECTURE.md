# 🏗️ Arquitectura Refactorizada - Audio Recorder & Opportunity Manager

## 📋 Resumen Ejecutivo

Se ha refactorizado completamente la arquitectura del proyecto para separar responsabilidades siguiendo patrones profesionales de software engineering:

- ✅ **Separación de Capas**: Frontend (Streamlit) desacoplado de lógica de negocio
- ✅ **Seguridad Reforzada**: Todas las credenciales centralizadas en `.env`
- ✅ **Validación de Datos**: Validadores en la capa de negocio antes de persistir
- ✅ **Mantenimiento Simplificado**: Código organizado y reutilizable
- ✅ **Funcionalidad Preservada**: El comportamiento del usuario permance igual

## 📁 Estructura de Carpetas

```
appGrabacionAudio/
├── .env                          # Variables de entorno (NO COMMITAR)
├── .env.example                  # Ejemplo de variables de entorno
├── .gitignore                    # Incluir .env, __pycache__, venv/
│
├── backend/                      # 🔧 CAPA DE NEGOCIO
│   ├── __init__.py
│   ├── config.py                 # Centralización de configuraciones
│   ├── supabase_client.py        # Cliente único de Supabase (singleton)
│   ├── validators.py             # Validadores de datos
│   │
│   ├── database/                 # 🗄️ CAPA DE ACCESO A DATOS
│   │   ├── __init__.py
│   │   ├── repositories.py       # Repositories pattern (CRUD)
│   │   └── schemas.py            # Esquemas de datos
│   │
│   └── services/                 # 🎯 SERVICIOS DE NEGOCIO
│       ├── __init__.py
│       ├── audio_service.py      # Lógica de grabaciones
│       ├── transcription_service.py  # Lógica de transcripciones
│       └── opportunity_service.py    # Lógica de oportunidades
│
├── ui/                           # 🎨 UI SHARED
│   ├── __init__.py
│   ├── styles.py                 # CSS/Estilos
│   └── notifications.py          # Componentes de notificación
│
├── index.py                      # 💻 FRONTEND STREAMLIT (punto de entrada)
├── Model.py                      # Gemini Model Integration
├── AudioRecorder.py              # Utilidades de grabación
├── Transcriber.py                # Utilidades de transcripción
├── OpportunitiesManager.py       # Utilidades de oportunidades (pendiente refactor)
│
├── requirements.txt              # Dependencias
├── BASEDEDATOS_SUPABASE.sql      # Schema de BD
└── ARCHITECTURE.md               # Este archivo
```

## 🏛️ Arquitectura de Capas

```
┌─────────────────────────────────────────┐
│        FRONTEND (Streamlit UI)          │  <- index.py
│   - Componentes visuales                │
│   - Interacción con usuaario            │
└─────────────────┬───────────────────────┘
                  │ Importa y usa servicios
┌─────────────────▼───────────────────────┐
│     SERVICES LAYER                      │  <- backend/services/
│   - AudioService                        │
│   - TranscriptionService                │
│   - OpportunityService                  │
│   - Contiene lógica de negocio          │
│   - Maneja validaciones                 │
│   - Orquesta repositories               │
└─────────────────┬───────────────────────┘
                  │ Usa repositories
┌─────────────────▼───────────────────────┐
│   REPOSITORIES LAYER                    │  <- backend/database/
│   - RecordingRepository                 │
│   - TranscriptionRepository             │
│   - OpportunityRepository               │
│   - CRUD encapsulado                    │
│   - Acceso directo a BD                 │
└─────────────────┬───────────────────────┘
                  │ Usa cliente
┌─────────────────▼───────────────────────┐
│   DATA ACCESS LAYER                     │  <- backend/supabase_client.py
│   - SupabaseClient (singleton)          │
│   - Una única conexión                  │
│   - Caché con Streamlit                 │
└─────────────────┬───────────────────────┘
                  │ Conecta a
┌─────────────────▼───────────────────────┐
│   EXTERNAL - Supabase BD                │
│   - PostgreSQL                          │
│   - Tablas: recordings, transcriptions  │
│   |         opportunities               │
└─────────────────────────────────────────┘
```

## 🔐 Seguridad - Gestión de Credenciales

### ❌ ANTES (Inseguro)
```python
# Credenciales hardcodeadas o en múltiples lugares
supabase_url = "https://xyz.supabase.co"
supabase_key = "eyJhbGciOiJI..."  # ¡Nunca hagas esto!
```

### ✅ AHORA (Seguro)
```
1. Crear archivo .env (NO COMMITAR - incluir en .gitignore)
2. Cargar en backend/config.py
3. Frontend obtiene credenciales desde Config

Flujo:
.env → config.py → supabase_client.py → repositories.py
```

### Archivo `.secrets.toml` de Streamlit (Optional)
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
GEMINI_API_KEY = "your-key"
```

## 📝 Ejemplo de Uso - Frontend (index.py)

### Antes (Acoplado, inseguro)
```python
# ❌ EVITAR
import database as db_utils
from supabase import create_client

# Conexión duplicada
supabase_url = st.secrets.get("SUPABASE_URL")
response = create_client(supabase_url, key).table("recordings").select("*").execute()

# Handle de errores con st.success (UI en la lógica)
if success:
    st.success("Guardado!")
```

### Después (Desacoplado, seguro)
```python
# ✅ RECOMENDADO
from backend.services import AudioService, OpportunityService

# Usar servicios
audio_service = AudioService()

# Guardar grabación
recording_id = audio_service.save_recording(filename, filepath)

# Las notificaciones están separadas en UI
if recording_id:
    show_success(f"Grabado con ID {recording_id}")
```

## 🔄 Flujos de Negocio Refactorizados

### 1. Guardar Grabación

```
index.py
  ↓
audio_service.save_recording(filename, filepath)
  ↓
AudioService.save_recording()
  ↓
RecordingRepository.create(filename, filepath)
  ↓
DataValidator.validate_recording()  ← Validación
  ↓
SupabaseClient.get_client()  ← Conexión única
  ↓
→ Supabase (BD)
```

### 2. Guardar Transcripción

```
index.py
  ↓
transcription_service.save_transcription(recording_id, content)
  ↓
TranscriptionService.save_transcription()
  ├─ RecordingRepository.get_by_id()  ← Verificar que existe
  ├─ TranscriptionRepository.create()
  │  └─ DataValidator.validate_transcription()
  └─ RecordingRepository.update_transcription()  ← Actualizar preview
  ↓
→ Supabase (BD)
```

### 3. Eliminar Grabación (Con Cascada)

```
index.py
  ↓
audio_service.delete_recording(recording_id)
  ↓
RecordingRepository.delete(recording_id)
  ├─ TranscriptionRepository.delete_by_recording()  ← Eliminar deps
  ├─ OpportunityRepository.delete_by_recording()    ← Eliminar deps
  └─ RecordingRepository.delete()  ← Eliminar registro
  ↓
→ Supabase (BD)
```

## 💾 Validaciones Integradas

Todas las validaciones ocurren en el backend ANTES de persistir:

```python
# backend/validators.py

DataValidator.validate_recording()
  ✓ Filename requerido, string, max 255 chars
  ✓ Filepath requerido, string
  ✓ Datos tipo diccionario

DataValidator.validate_transcription()
  ✓ Content requerido, string
  ✓ Recording_id requerido
  ✓ Content max 50000 chars

DataValidator.validate_opportunity()
  ✓ Title requerido, string
  ✓ Recording_id requerido
  ✓ Description max 5000 chars
```

Si la validación falla, lanza excepción → capturada en service → retorna None/False

## 🚀 Cómo Usar los Servicios

### AudioService
```python
from backend.services import AudioService

audio_service = AudioService()

# Guardar
recording_id = audio_service.save_recording("audio.wav", "/path/to/audio.wav")

# Obtener todos
recordings = audio_service.get_all_recordings()

# Obtener específico
recording = audio_service.get_recording(recording_id)

# Buscar por nombre
recording = audio_service.get_recording_by_filename("audio.wav")

# Eliminar (con cascada)
success = audio_service.delete_recording(recording_id)
```

### TranscriptionService
```python
from backend.services import TranscriptionService

trans_service = TranscriptionService()

# Guardar
trans_id = trans_service.save_transcription(
    recording_id=123,
    content="Transcripción completa del audio...",
    language="es"
)

# Obtener
transcription = trans_service.get_transcription(recording_id=123)
print(transcription["content"])

# Actualizar
success = trans_service.update_transcription(recording_id=123, content="Nueva transcripción")
```

### OpportunityService
```python
from backend.services import OpportunityService

opp_service = OpportunityService()

# Crear oportunidad individual
opp_id = opp_service.create_opportunity(
    recording_id=123,
    title="Nueva Oportunidad",
    description="Descripción completa..."
)

# Obtener oportunidades de un recording
opportunities = opp_service.get_opportunities_by_recording(recording_id=123)

# Extraer automáticamente desde palabras clave
keywords = {"cliente": {}, "presupuesto": {}, "reunión": {}}
created_ids = opp_service.extract_opportunities_from_keywords(
    recording_id=123,
    transcription="Cliente habló sobre presupuesto en la reunión...",
    keywords=keywords
)
```

## ⚙️ Configuración Global

```python
# backend/config.py
from backend.config import Config

# Acceder a configuraciones
Config.SUPABASE_URL          # URL de Supabase
Config.SUPABASE_KEY          # Key de Supabase
Config.GEMINI_API_KEY        # API Key de Gemini
Config.RECORDINGS_DIR        # Directorio de grabaciones
Config.OPPORTUNITIES_DIR     # Directorio de oportunidades

# Validar que existen credenciales necesarias
Config.validate()  # Lanza error si falta algo
```

## 📊 Relaciones de BD (Integridad)

```sql
recordings
├─ id (PK)
├─ filename
├─ filepath
├─ transcription (preview)
└─ created_at

transcriptions (1:1 con recordings)
├─ id (PK)
├─ recording_id (FK → recordings)
├─ content
├─ language
└─ created_at

opportunities (N:1 con recordings)
├─ id (PK)
├─ recording_id (FK → recordings)
├─ title
├─ description
└─ created_at
```

**Integridad**: Cuando se elimina un recording:
1. Se eliminan todas sus transcripciones
2. Se eliminan todas sus oportunidades
3. Se elimina el recording (cascada)

## 🧪 Testing Recomendado

```python
# Ejemplo: test_audio_service.py
from backend.services import AudioService

def test_save_recording():
    service = AudioService()
    recording_id = service.save_recording("test.wav", "/path/test.wav")
    assert recording_id is not None
    assert isinstance(recording_id, int)

def test_duplicate_filename():
    # Validar que no permite guardar con mismo nombre
    service = AudioService()
    service.save_recording("dup.wav", "/path/1.wav")
    # ¿Segunda vez retorna None o actualiza?

def test_invalid_data():
    # Validar que rechaza datos inválidos
    service = AudioService()
    with pytest.raises(ValueError):
        service.save_recording("", "")
```

## 📈 Ventajas de la Refactorización

| Aspecto | Antes | Después |
|--------|--------|---------|
| **Seguridad Credenciales** | Hardcoded/disperso | Centralizado en .env |
| **Validación Datos** | En UI | En backend (antes de persistir) |
| **Acoplamiento** | Streamlit ↔ BD directa | Desacoplado via servicios |
| **Mantenimiento** | Cambios en muchos archivos | Cambios localizados |
| **Testing** | Difícil (UI + Logic) | Fácil (servicios sin UI) |
| **Reutilización** | Limitala | Máxima (servicios indep.) |
| **Errores Silenciosos** | ❌ | ✅ Logs en backend |
| **Escalabilidad** | Limitada | Preparada para APIs REST |

## 🔄 Próximos Pasos

1. **API REST** (Optional): Usar FastAPI para exponer servicios como API
2. **Tests**: Agregar tests unitarios para los servicios
3. **Logging**: Sistema de logging centralizado (no print)
4. **Async**: Operaciones async para BD y APIs
5. **Rate Limiting**: Proteger servicios de abuso
6. **Authentication**: SI se crea API, agregar JWT tokens

## 📚 Referencia Rápida

```python
# El frontend solo importa servicios, NUNCA accede a BD
from backend.services import AudioService, TranscriptionService, OpportunityService

# Inicializar servicios
audio_svc = AudioService()
trans_svc = TranscriptionService()
opp_svc = OpportunityService()

# El backend se encarga de todo lo demás
recording_id = audio_svc.save_recording(filename, filepath)
trans_id = trans_svc.save_transcription(recording_id, content)
opp_id = opp_svc.create_opportunity(recording_id, title, desc)
```

---

**Autor**: Arquitectura Refactorizada para Audio Recorder & Opportunity Manager  
**Fecha**: 2026-02-06  
**Versión**: 2.0 (Refactorizada)
