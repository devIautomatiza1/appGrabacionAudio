# 📋 DOCUMENTACIÓN COMPLETA DEL PROYECTO

## 🎯 VISIÓN GENERAL

**Nombre del Proyecto:** Audio Recorder & Opportunity Manager  
**Objetivo:** Convertir audios en inteligencia de negocio automáticamente  
**Tipo:** Aplicación web interactiva basada en Streamlit  
**Fecha de Creación:** 2026-02-06  
**Estado:** En producción con features completas

---

## 📚 TABLA DE CONTENIDOS

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Arquitectura General](#arquitectura-general)
3. [Base de Datos](#base-de-datos)
4. [Stack Tecnológico](#stack-tecnológico)
5. [Módulos del Código](#módulos-del-código)
6. [Flujo de Datos](#flujo-de-datos)
7. [Características Principales](#características-principales)
8. [Instrucciones de Configuración](#instrucciones-de-configuración)
9. [Estado Actual](#estado-actual)
10. [Roadmap Futuro](#roadmap-futuro)

---

## 📱 DESCRIPCIÓN DEL PROYECTO

### Problema que Resuelve

En empresas de ventas, atención al cliente y negocios:
- Hay muchas **conversaciones/llamadas** que generan información valiosa
- Extraer esa información **manualmente es tedioso y lento**
- Se pierden **oportunidades de negocio** por falta de seguimiento
- No hay forma de **rastrear y gestionar tickets** de audio

### Solución Implementada

Una aplicación que:
1. **Captura audios** (grabación directa o upload)
2. **Transcribe automáticamente** usando IA (Gemini/OpenAI)
3. **Extrae oportunidades de negocio** basadas en palabras clave
4. **Crea tickets** con estado, prioridad y notas
5. **Almacena todo en la nube** (Supabase) para acceso compartido
6. **Permite chat interactivo** con IA sobre los audios

### Casos de Uso

✅ **Centro de Atención al Cliente** - Capturar insights de llamadas  
✅ **Ventas B2B** - Rastrear oportunidades mencionadas en conversaciones  
✅ **Consultoría** - Documentar reuniones y extraer accionables  
✅ **RH** - Análisis de feedback en entrevistas  
✅ **Auditoría/Compliance** - Registro y revisión de comunicaciones  

---

## 🏗️ ARQUITECTURA GENERAL

### Diagrama de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB APP                            │
│                   (index.py - Main File)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────┐  ┌─────────────────┐  ┌──────────────────┐ │
│  │  GRABACIÓN     │  │  TRANSCRIPCIÓN  │  │  ANÁLISIS IA     │ │
│  │  DE AUDIOS     │  │  AUTOMÁTICA     │  │  CON PALABRAS    │ │
│  │                │  │                 │  │  CLAVE           │ │
│  │ AudioRecorder  │  │ Transcriber.py  │  │ OpportunitiesM.  │ │
│  │                │  │                 │  │                  │ │
│  └────────────────┘  └─────────────────┘  └──────────────────┘ │
│           ↓                   ↓                      ↓           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │            SUPABASE (PostgreSQL)                          │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐   │ │
│  │  │ recordings  │  │ transcriptions│ │ opportunities  │   │ │
│  │  │  TABLE      │  │    TABLE     │  │    TABLE       │   │ │
│  │  └─────────────┘  └──────────────┘  └────────────────┘   │ │
│  └────────────────────────────────────────────────────────────┘ │
│           ↑                   ↑                      ↑           │
│  ┌────────────────┐  ┌─────────────────┐  ┌──────────────────┐ │
│  │  GESTIÓN BD    │  │   CHAT CON IA   │  │   DEBUG/MONITOR  │ │
│  │  database.py   │  │   Model.py      │  │   (Contador)     │ │
│  └────────────────┘  └─────────────────┘  └──────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Flujo de Componentes

```
Usuario Interactúa
    ↓
┌─ Graba o Carga Audio ─→ AudioRecorder.py ─→ Guarda en Supabase
│
├─ Presiona "Transcribir" ─→ Transcriber.py ─→ Guarda en tabla transcriptions
│
├─ Define 100 Palabras Clave ─→ OpportunitiesManager.py ─→ Busca en transcripción
│
├─ "Generar Oportunidades" ─→ Crea Tickets ─→ Guarda en opportunities table
│
├─ Edita Tickets (estado, prioridad, notas) ─→ database.py ─→ Actualiza Supabase
│
└─ Chatea con IA ─→ Model.py ─→ Usa contexto de audio + palabras clave
```

---

## 🗄️ BASE DE DATOS

### Estructura Visual (Supabase PostgreSQL)

```
PROJECT: appgrabacionaudio
├── Table: public.recordings
│   ├── id (uuid, PK)
│   ├── filename (text)
│   ├── filepath (text)
│   ├── transcription (text) [DEPRECATED - usar tabla transcriptions]
│   ├── created_at (timestamp)
│   └── updated_at (timestamp)
│
├── Table: public.transcriptions [NEW - Feb 2026]
│   ├── id (uuid, PK)
│   ├── recording_id (uuid, FK → recordings.id, ON DELETE CASCADE)
│   ├── content (text)
│   ├── language (text, default='es')
│   ├── created_at (timestamp)
│   └── updated_at (timestamp)
│
└── Table: public.opportunities
    ├── id (uuid, PK)
    ├── recording_id (uuid, FK → recordings.id)
    ├── title (text)
    ├── description (text)
    ├── status (text: 'new', 'in_progress', 'closed', 'won')
    ├── priority (text: 'Low', 'Medium', 'High')
    ├── ticket_number (int4)
    ├── notes (text) [NEW - Feb 2026]
    └── created_at (timestamp)
```

### Relaciones entre Tablas

```
recordings (1) ──────╬───────── (N) transcriptions
                     │
                     │ ON DELETE CASCADE
                     │
recordings (1) ──────╬───────── (N) opportunities
```

### Descripción Detallada de Campos

#### Tabla: recordings
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | uuid | Identificador único del audio |
| filename | text | Nombre archivo (ej: "meeting_2026-02-06.wav") |
| filepath | text | Ruta en Supabase Storage |
| transcription | text | ⚠️ DEPRECATED - usar tabla transcriptions |
| created_at | timestamp | Fecha de carga |
| updated_at | timestamp | Última actualización |

#### Tabla: transcriptions
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | uuid | ID único de la transcripción |
| recording_id | uuid | FK al audio original |
| content | text | Texto completo transcrito |
| language | text | Código idioma (es, en, fr, de, etc) |
| created_at | timestamp | Fecha de transcripción |
| updated_at | timestamp | Última modificación |

**Nota:** Permite múltiples transcripciones por audio (versionado)

#### Tabla: opportunities
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | uuid | ID único del ticket |
| recording_id | uuid | FK al audio que generó el ticket |
| title | text | Palabra clave encontrada (ej: "presupuesto") |
| description | text | Contexto completo (15 palabras antes/después) |
| status | text | Estado workflow (new/in_progress/closed/won) |
| priority | text | Urgencia (Low/Medium/High) |
| ticket_number | int4 | Número secuencial para referencia rápida |
| notes | text | Resumen/análisis agregado por usuario |
| created_at | timestamp | Fecha de generación |

---

## 💻 STACK TECNOLÓGICO

### Frontend
- **Framework:** Streamlit 1.32.0
- **Lenguaje:** Python 3.14
- **UI Components:** Built-in Streamlit widgets
- **Audio Playback:** Native HTML5 audio

### Backend
- **Lenguaje:** Python 3.14
- **Servidor:** Streamlit Cloud (deployable) / Local dev

### Base de Datos
- **Platform:** Supabase (PostgreSQL managed)
- **Auth:** API Keys (sin Supabase Auth configurado aún)
- **Storage:** Supabase Storage (para archivos de audio)
- **ORM Approach:** Custom lightweight client (para evitar storage3 dependency)

### APIs Externas
- **Transcripción:** Google Generative AI (Gemini) OR OpenAI
- **Chat/IA:** OpenAI GPT / Google Gemini
- **Secrets Management:** Streamlit Secrets (`.streamlit/secrets.toml`)

### Dependencias Principales
```
streamlit==1.32.0
python-dotenv
google-generative-ai (for Gemini)
openai (for OpenAI)
httpx (for custom Supabase client)
postgrest (for DB queries)
pydantic (for validation)
audio-recorder-streamlit (for recording)
websockets
deprecation
```

### Desarrollo
- **IDE:** VS Code
- **Version Control:** Git/GitHub
- **Environment:** Virtual Environment (`.venv`)
- **Package Manager:** pip

---

## 📂 MÓDULOS DEL CÓDIGO

### 1. index.py (Archivo Principal)
**Responsabilidad:** Orquestar toda la aplicación Streamlit

**Secciones Principales:**
```python
1. INICIALIZACIÓN
   - Cargar secrets
   - Inicializar session_state
   - Importar módulos

2. SECCIÓN GRABACIÓN/CARGA DE AUDIOS
   - Grabadora de micrófono
   - Upload de archivos
   - Guardar en Supabase

3. SECCIÓN LISTADO DE AUDIOS
   - Mostrar audios desde Supabase
   - Selectbox para elegir audio
   - Cargar transcripción si existe

4. SECCIÓN TRANSCRIPCIÓN
   - Mostrar transcripción
   - Botón "Transcribir"
   - Guardar en tabla transcriptions

5. SECCIÓN PALABRAS CLAVE
   - Input para agregar palabras clave
   - Mostrar palabras clave agregadas
   - Botón "Generar Oportunidades"

6. SECCIÓN OPORTUNIDADES
   - Mostrar tickets generados
   - Editar estado, prioridad, notas
   - Guardar cambios en Supabase
   - Eliminar tickets

7. SECCIÓN CHAT
   - Chat interactivo con IA
   - Contexto de transcripción
   - Palabras clave disponibles

8. SECCIÓN DEBUG
   - Contador de grabaciones
   - Contador de oportunidades
   - Contador de transcripciones
   - Estado de conexión a Supabase
```

**Session State Variables:**
```python
st.session_state.contexto          # Texto de la transcripción
st.session_state.selected_audio    # Audio actualmente seleccionado
st.session_state.loaded_audio      # Último audio cargado (evita loop)
st.session_state.chat_enabled      # Mostrar sección de chat
st.session_state.keywords          # Dict de palabras clave {palabra: contexto}
st.session_state.recordings        # Lista de audios disponibles
st.session_state.chat_history      # Historial de conversación
```

---

### 2. AudioRecorder.py
**Responsabilidad:** Gestionar grabación, carga y lista de audios

**Funciones Principales:**
```python
class AudioRecorder:
    def __init__()
        # Inicializar grabador
    
    def start_recording()
        # Iniciar grabación de micrófono
    
    def stop_recording() → audio_path
        # Detener y guardar archivo
    
    def get_recordings_list() → List[str]
        # Listar audios locales [DEPRECATED]
    
    def get_recordings_from_supabase() → List[str]
        # Listar audios desde Supabase ✅ [ACTUAL]
        # Retorna [filename1, filename2, ...]
    
    def save_recording(filename, filepath)
        # Guardar metadata en Supabase
    
    def delete_recording(filename)
        # Eliminar audio local
    
    def get_recording_path(filename) → str
        # Obtener ruta del archivo para reproducción
```

---

### 3. Transcriber.py
**Responsabilidad:** Convertir audio a texto

**Funciones Principales:**
```python
class AudioTranscriber:
    def __init__(api_key)
        # Inicializar cliente de IA (Gemini/OpenAI)
    
    def transcript_audio(audio_path) → TranscriptionResult
        # Transcribir archivo de audio
        # Retorna: obj con .text (transcripción)
```

**Flujo:**
```
Audio File → Load to Memory → Send to API → Get Text
```

---

### 4. OpportunitiesManager.py
**Responsabilidad:** Extraer oportunidades y gestionar tickets

**Funciones Principales:**
```python
class OpportunitiesManager:
    def __init__()
        # Conectar a Supabase
    
    def extract_opportunities(transcription, keywords_list) → List[dict]
        # CORE LOGIC: Busca TODAS las ocurrencias de palabras clave
        # Retorna lista de oportunidades con:
        # {
        #   id, keyword, full_context,
        #   status, priority, notes,
        #   created_at, occurrence
        # }
    
    def save_opportunity(opportunity, audio_filename) → bool
        # Guardar ticket en tabla opportunities de Supabase
        # Obtiene recording_id buscando por filename
    
    def load_opportunities(audio_filename) → List[dict]
        # Cargar todos los tickets de un audio desde Supabase
    
    def update_opportunity(opportunity, audio_filename) → bool
        # Actualizar estado, prioridad, notas en Supabase
    
    def delete_opportunity(opportunity_id, audio_filename) → bool
        # Eliminar ticket de Supabase
```

**Lógica de Extracción de Oportunidades:**
```
Input: Transcripción + ["presupuesto", "reunión", "contrato"]
Process:
  Para cada palabra clave:
    Buscar TODAS las ocurrencias en el texto
    Para cada ocurrencia:
      Extraer 15 palabras antes y después (contexto)
      Crear opportunity con ese contexto
Output: Lista de opportunities con contexto
```

---

### 5. Model.py
**Responsabilidad:** Interacción con APIs de IA para chat

**Funciones Principales:**
```python
class ChatModel:
    def __init__(api_key)
        # Inicializar cliente OpenAI/Gemini
    
    def call_model(user_input, transcription, keywords) → str
        # Sistema de prompt que:
        # 1. Proporciona contexto de la transcripción
        # 2. Incluye palabras clave como variables
        # 3. Responde pregunta del usuario
        
        # Ejemplo de contexto:
        # "El usuario está analizando un audio donde se menciona:
        #  Audio: '{transcription[:500]}...'
        #  Palabras clave identificadas: {list(keywords.keys())}
        #  Pregunta del usuario: '{user_input}'"
```

---

### 6. database.py
**Responsabilidad:** CRUD en Supabase

**Funciones Principales:**

#### Inicialización
```python
def init_supabase() → Client
    # Crear conexión con Supabase usando secrets
    # Cached con @st.cache_resource para evitar múltiples conexiones
```

#### Grabaciones (recordings)
```python
def save_recording_to_db(filename, filepath, transcription=None) → str
    # Insertar en tabla recordings
    # Retorna: recording_id

def get_all_recordings() → List[dict]
    # SELECT * FROM recordings

def delete_recording_from_db(recording_id) → bool
    # Eliminar por ID y sus oportunidades asociadas

def delete_recording_by_filename(filename) → bool
    # Eliminar por nombre de archivo
```

#### Transcripciones (transcriptions) ✅
```python
def save_transcription(recording_filename, content, language='es') → str
    # Insertar en tabla transcriptions
    # Busca recording_id por filename
    # Retorna: transcription_id

def get_transcription_by_filename(recording_filename) → dict
    # Obtener transcripción más reciente de un audio
    # Retorna: {id, content, language, created_at, ...}

def delete_transcription_by_id(transcription_id) → bool
    # Eliminar transcripción específica
```

#### Oportunidades (opportunities)
```python
def save_opportunity(recording_id, title, description) → bool
    # Insertar en tabla opportunities

def get_opportunities_by_recording(recording_id) → List[dict]
    # SELECT * FROM opportunities WHERE recording_id = ?

def delete_opportunities_by_recording(recording_id) → bool
    # Eliminar todos los tickets de un audio (CASCADE)
```

---

## 📊 FLUJO DE DATOS

### Flujo #1: Grabación/Carga de Audio

```
User Clicks "Grabar" or "Cargar Archivo"
        ↓
AudioRecorder.py obtiene audio
        ↓
database.save_recording_to_db(filename, filepath)
        ↓
INSERT INTO recordings (filename, filepath, created_at)
        ↓
session_state.recordings = get_recordings_from_supabase()
        ↓
Mostrar en dropdown
```

---

### Flujo #2: Transcripción

```
User Selects Audio + Clicks "Transcribir"
        ↓
Transcriber.transcript_audio(audio_path)
        ↓
API (Gemini/OpenAI): Audio → Text
        ↓
database.save_transcription(filename, text, 'es')
        ↓
INSERT INTO transcriptions (recording_id, content, language)
        ↓
session_state.contexto = transcription.text
        ↓
Mostrar en text_area
```

---

### Flujo #3: Generar Oportunidades

```
User Adds Keywords + Clicks "Generar Oportunidades"
        ↓
keywords_list = ["presupuesto", "reunión", ...]
        ↓
OpportunitiesManager.extract_opportunities(transcription, keywords)
        ↓
Para cada keyword:
  Busca todas las ocurrencias
  Extrae contexto (15 palabras antes/después)
  Crea opportunity dict
        ↓
Para cada opportunity:
  database.save_opportunity(opportunity, filename)
        ↓
INSERT INTO opportunities (recording_id, title, description, status, priority)
        ↓
Mostrar en expanders con estado/prioridad/notas editables
```

---

### Flujo #4: Editar Ticket

```
User Changes Estado/Prioridad/Notas + Clicks "Guardar Cambios"
        ↓
opp['status'] = new_status
opp['priority'] = new_priority
opp['notes'] = new_notes
        ↓
OpportunitiesManager.update_opportunity(opp, filename)
        ↓
UPDATE opportunities SET status=?, priority=?, notes=? WHERE id=?
        ↓
st.success("✅ Cambios guardados en Supabase")
```

---

### Flujo #5: Chat con IA

```
User Types Question
        ↓
Model.call_model(user_input, transcription, keywords)
        ↓
IA System Prompt Incluye:
  - Transcripción (contexto)
  - Palabras clave (variables)
  - Pregunta del usuario
        ↓
API Response
        ↓
st.session_state.chat_history.append(user + response)
        ↓
Mostrar en chat interface
```

---

## ✨ CARACTERÍSTICAS PRINCIPALES

### 1. Grabación de Audio ✅
- **Método:** Micrófono del dispositivo
- **Formats Soportados:** WAV, MP3, M4A, WebM, OGG, FLAC
- **Almacenamiento:** Supabase Storage + Metadata en tabla recordings

### 2. Upload de Archivos ✅
- Drag & drop o click para seleccionar
- Validación de formato
- Progreso de carga

### 3. Listado desde Supabase ✅
- Dropdown con todos los audios disponibles
- Se actualiza automáticamente
- Mostrar audio seleccionado en reproductor

### 4. Transcripción Automática ✅
- Botón "Transcribir"
- Usa API externa (Gemini/OpenAI)
- Guarda en tabla transcriptions
- Carga automática si ya existe

### 5. Palabras Clave Contextualizadas ✅
- Usuario agrega palabras clave customizadas
- Describe contexto para cada una
- Se usan en chat y extracción de oportunidades

### 6. Extracción de Oportunidades ✅
- Busca TODAS las ocurrencias de palabras clave
- Extrae contexto (15 palabras antes y después)
- Crea tickets automáticamente
- Guarda en tabla opportunities

### 7. Gestión de Tickets ✅
- Ver todos los tickets de un audio
- Editar estado (new, in_progress, closed, won)
- Editar prioridad (Low, Medium, High)
- Agregar notas/resumen
- Eliminar tickets
- Persistencia en Supabase

### 8. Chat Interactivo con IA ✅
- Chat interface integrada
- Contexto: transcripción + palabras clave
- Historial de conversación
- Múltiples vueltas de preguntas/respuestas

### 9. Debug & Monitoring ✅
- Contador de grabaciones en BD
- Contador de oportunidades en BD
- Contador de transcripciones en BD
- Estado de conexión a Supabase

### 10. Persistencia de Datos ✅
- Todo guardado en Supabase PostgreSQL
- Accessible desde cualquier dispositivo
- Sincronización en tiempo real
- Cascade delete cuando se elimina audio

---

## 🔧 INSTRUCCIONES DE CONFIGURACIÓN

### Prerequisitos
- Python 3.14+
- Virtual Environment
- Cuenta Supabase (free tier es suficiente)
- API Keys: Gemini (Google) Y/O OpenAI

### 1. Clonar Repositorio
```bash
git clone https://github.com/tu-usuario/appGrabacionAudio.git
cd appGrabacionAudio
```

### 2. Crear Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Secrets (Streamlit)

Crear archivo `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
GEMINI_API_KEY = "AIzaSyD..."
OPENAI_API_KEY = "sk-xxx..."
```

### 5. Crear Tablas en Supabase

Copiar y ejecutar en SQL Editor de Supabase:
```sql
-- Ver archivo: transcriptions_schema.sql
CREATE TABLE public.recordings (...)
CREATE TABLE public.transcriptions (...)
CREATE TABLE public.opportunities (...)
```

### 6. Run Local
```bash
streamlit run index.py
```

Abrirá en `http://localhost:8501`

### 7. Deploy a Streamlit Cloud (Opcional)
```bash
git push origin main
# Settings → Connect Repository → Select appGrabacionAudio
```

---

## 📊 ESTADO ACTUAL

### ✅ Features Completadas (Feb 2026)

| Feature | Status | Notas |
|---------|--------|-------|
| Grabación de audio | ✅ | Funcional con micrófono |
| Upload de archivos | ✅ | Soporta múltiples formatos |
| Listar desde Supabase | ✅ | Se sincroniza automáticamente |
| Reproducción | ✅ | Integrada en UI |
| Transcripción | ✅ | Guarda en tabla transcriptions |
| Palabras clave | ✅ | Customizables por usuario |
| Extracción de oportunidades | ✅ | Busca todas las ocurrencias |
| Gestión de tickets | ✅ | CRUD completo en Supabase |
| Chat con IA | ✅ | Con contexto de audio |
| Debug/Monitoring | ✅ | 3 contadores en tiempo real |
| Persistencia de datos | ✅ | Todo en Supabase |

### 🔄 En Desarrollo
- (Ninguno actualmente - versión estable)

### 📋 Próximas Mejoras Sugeridas
- [ ] Autenticación con Supabase Auth
- [ ] Multi-usuario con permisos
- [ ] Búsqueda y filtrado de tickets
- [ ] Exportar análisis a PDF/Excel
- [ ] Webhook para notificaciones
- [ ] API REST para integración
- [ ] Análisis sentimiento en transcripciones
- [ ] Traducción automática
- [ ] Grabación en Streaming (no solo archivos)

---

## 🗂️ ESTRUCTURA DE ARCHIVOS

```
appGrabacionAudio/
├── index.py                          # Aplicación principal
├── AudioRecorder.py                  # Gestión de audios
├── Transcriber.py                    # Transcripción
├── Model.py                          # Chat con IA
├── OpportunitiesManager.py           # Extracción y gestión de tickets
├── database.py                       # Funciones CRUD para Supabase
│
├── .streamlit/
│   └── secrets.toml                  # 🔐 Secrets (NO commit a Git)
│
├── requirements.txt                  # Dependencias Python
├── .gitignore                        # Archivos ignorados en Git
├── .env                              # Variables de entorno locales
│
├── recordings/                       # Carpeta local de audios (local dev)
├── opportunities/                    # Carpeta JSON (DEPRECATED - usar Supabase)
│
├── PROJECT_DOCUMENTATION.md          # Este archivo
├── TRANSCRIPTIONS_SETUP.md           # Guía de tabla transcriptions
├── transcriptions_schema.sql         # SQL para crear tabla
│
└── test/
    ├── test_supabase.py             # Tests de conexión
    └── test_supabase_simple.py
```

---

## 🔐 Seguridad & Best Practices

### Secrets Management ✅
- `.env` existe pero NO se commiteó
- Secrets almacenados en `.streamlit/secrets.toml`
- `.gitignore` previene leaks de credenciales

### Row Level Security (RLS)
- RLS está DESHABILITADO actualmente (desarrollo)
- Para producción: Implementar Supabase Auth + RLS policies

### HTTPS/SSL
- Streamlit Cloud automáticamente usa HTTPS
- Desarrollo local: solo para testing

---

## 🚀 Cómo Contribuir

1. **Branch Nueva Features**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

2. **Hacer Cambios**
   - Editar archivos necesarios
   - Probar localmente con `streamlit run index.py`

3. **Commit & Push**
   ```bash
   git add .
   git commit -m "feat: descripción de cambios"
   git push origin feature/nueva-funcionalidad
   ```

4. **Pull Request**
   - Describir cambios en PR
   - Esperar review

---

## 📞 Soporte & Troubleshooting

### Error: "Conexión a Supabase fallida"
- Verificar SUPABASE_URL y SUPABASE_KEY en secrets
- Comprobar que no hay espacios en blanco
- Confirmar que RLS esté deshabilitado

### Error: "Módulo X no encontrado"
```bash
pip install -r requirements.txt
```

### Transcripción lenta
- APIs (Gemini/OpenAI) pueden tardar 5-30 segundos
- Normal para archivos largos

### Página se recarga en loop
- Problema: `st.rerun()` sin condición
- Solución: Usar flags tipo `loaded_audio` para evitar reload recursivo

---

## 📈 Métricas & Analytics

### Datos Disponibles en Debug
```
✅ Grabaciones en BD: Contador de audios
✅ Oportunidades en BD: Contador de tickets
✅ Transcripciones en BD: Contador de textos
```

Expandible a:
- Promedio de tickets por audio
- Palabras clave más frecuentes
- Tiempo promedio de transcripción
- Tickets resueltos vs abiertos

---

## 🎓 Referencias & Documentación Externa

- **Streamlit Docs:** https://docs.streamlit.io
- **Supabase Docs:** https://supabase.com/docs
- **Google Gemini API:** https://ai.google.dev/
- **OpenAI API:** https://openai.com/docs
- **PostgreSQL Docs:** https://www.postgresql.org/docs

---

## 📝 Licencia & Información

- **Autor:** Usuario del Proyecto
- **Fecha Creación:** 2026-02-06
- **Última Actualización:** 2026-02-06
- **Estado:** Producción
- **Versión:** 1.0 Stable

---

**Este documento sirve como "pasaporte" del proyecto para que cualquier IA o desarrollador pueda entender completamente su arquitectura, funcionalidad y estado actual.**

¿Preguntas? Revisar el código en los archivos `.py` para detalles específicos de implementación.
