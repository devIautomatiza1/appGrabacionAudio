# INFORME TÉCNICO
## Sistema Control Audio Iprevencion

---

## 1. INTRODUCCIÓN

**Proyecto:** Sistema Control Audio Iprevencion  
**Fecha:** Febrero 5, 2026  
**Estado:** En desarrollo  
**Versión:** 1.0

### Descripción General
Aplicación web desarrollada con Streamlit que permite grabar, subir, transcribir y gestionar archivos de audio utilizando inteligencia artificial para procesamiento de lenguaje natural.

---

## 2. FUNCIONALIDADES IMPLEMENTADAS

### 2.1 Grabación de Audio
- ✅ Grabadora nativa en vivo directamente desde el micrófono
- ✅ Detección automática de audios nuevos (mediante hash MD5)
- ✅ Prevención de duplicados en la base de datos
- ✅ Guardado automático sin necesidad de recargar página

### 2.2 Carga de Archivos
- ✅ Soporte para múltiples formatos: MP3, WAV, M4A, OGG, FLAC, WEBM
- ✅ Límite de 200MB por archivo
- ✅ Actualización dinámica del listado sin recargas

### 2.3 Gestión de Audios
- ✅ Listado de todos los audios grabados/cargados
- ✅ Reproducción de audio en la interfaz
- ✅ Eliminación individual de archivos
- ✅ Eliminación en lote (múltiples archivos)
- ✅ Contador total de audios guardados

### 2.4 Transcripción de Audio
- ✅ Integración con Google Generative AI (Gemini)
- ✅ Transcripción automática de audio a texto
- ✅ Visualización de transcripción en editor de texto

### 2.5 Interfaz de Usuario
- ✅ Diseño responsive con layout de dos columnas
- ✅ Badges de color (sin iconos emoji)
- ✅ Notificaciones modernas con efecto pulse
- ✅ Toast notifications discretas
- ✅ Tabs para diferentes vistas
- ✅ Tema personalizado (claro/oscuro seleccionable)

---

## 3. TECNOLOGÍAS UTILIZADAS

### Backend
- **Python 3.14** - Lenguaje de programación
- **Streamlit 1.31.1** - Framework web
- **google-generativeai 0.8.6** - API de Google para transcripción/IA
- **openai 1.3.7** - API de OpenAI (integración)
- **python-dotenv 1.0.0** - Gestión de variables de entorno

### Frontend
- **Streamlit Components** - Interfaz de usuario
- **HTML/CSS personalizado** - Estilos avanzados
- **JavaScript nativo del navegador** - Interactividad

### Almacenamiento
- **Sistema de archivos local** - Carpeta `/recordings/`
- **Estructura: `recording_YYYYMMDD_HHMMSS.wav`**

---

## 4. ESTRUCTURA DEL PROYECTO

```
appGrabacionAudio/
├── index.py                    # Aplicación principal
├── AudioRecorder.py            # Clase para grabación/gestión de audios
├── Transcriber.py              # Clase para transcripción con Gemini
├── Model.py                    # Clase para procesamiento con OpenAI
├── OpportunitiesManager.py     # Gestor de oportunidades
├── requirements.txt            # Dependencias del proyecto
├── .env                        # Variables de entorno (API keys)
├── .streamlit/
│   └── config.toml            # Configuración de Streamlit
├── recordings/                 # Carpeta de audios grabados/subidos
├── opportunities/              # Datos de oportunidades
└── README.md                   # Documentación del proyecto
```

---

## 5. CAMBIOS Y MEJORAS REALIZADAS

### 5.1 Eliminación de Dependencias Problemáticas
- ❌ Removida: `pyaudio` (incompatible con Python 3.14)
- ❌ Removida: `streamlit-webrtc` (requiere compiladores C)
- ❌ Removida: `av` (compilación fallida)
- ✅ Solución: Uso de `st.audio_input()` nativa de Streamlit

### 5.2 Mejora de Estado y Actualizaciones
- ✅ Implementado control de hash MD5 para detectar audios nuevos
- ✅ Eliminados `st.rerun()` innecesarios
- ✅ Uso de `st.session_state` para actualizaciones dinámicas
- ✅ La página NO recarga al grabar/subir archivos

### 5.3 Mejora de Interfaz
- ✅ Removidos todos los iconos emoji
- ✅ Implementados badges de color con fondo gradiente
- ✅ Título actualizado a "Sistema Control Audio Iprevencion"
- ✅ Notificaciones modernas con efecto pulse-glow
- ✅ Toast notifications sutiles con ✨

### 5.4 Configuración de Streamlit
- ✅ Desactivado modal de "Deploy"
- ✅ Selector de tema (claro/oscuro) habilitado
- ✅ Configuración personalizada en `.streamlit/config.toml`

---

## 6. FLUJO DE USUARIO

```
┌─────────────────────────────────────────────────────┐
│  1. Usuario accede a la aplicación                  │
│     http://localhost:8501                           │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   ┌────▼─────┐          ┌──────▼────┐
   │  GRABAR   │          │  SUBIR    │
   └────┬─────┘          └──────┬────┘
        │                       │
   ┌────▼──────────────────────▼────┐
   │  Audio guardado en /recordings/ │
   └────┬─────────────────────────────┘
        │
   ┌────▼────────────────────────────┐
   │  Aparece en desplegable          │
   │  (sin recargar página)           │
   └────┬────────────────────────────┘
        │
   ┌────▼────────────────────┐
   │  Usuario selecciona     │
   │  Reproducir/Transcribir │
   │  Eliminar               │
   └────┬────────────────────┘
        │
   ┌────▼─────────────────┐
   │  Acción completada   │
   │  Toast notification  │
   └──────────────────────┘
```

---

## 7. CONFIGURACIÓN NECESARIA

### 7.1 Variables de Entorno (`.env`)
```
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 7.2 Instalación
```bash
pip install -r requirements.txt
```

### 7.3 Ejecución
```bash
streamlit run index.py
```

---

## 8. ESTADO ACTUAL Y PROBLEMAS CONOCIDOS

### ✅ Funcionando correctamente
- Grabación de audio
- Carga de archivos
- Listado dinámico
- Eliminación de audios
- Interfaz responsive
- Tema claro/oscuro

### ⚠️ Problemas y Soluciones
1. **API Key expirada**
   - Causa: Google Generative AI requiere renovación periódica
   - Solución: Generar nueva key en [aistudio.google.com](https://aistudio.google.com/app/apikey)

2. **Sin base de datos centralizada**
   - Causa: Audios guardados localmente en `/recordings/`
   - Solución propuesta: Migrar a Supabase (próximo paso)

---

## 9. PRÓXIMOS PASOS RECOMENDADOS

### Fase 2: Despliegue en Internet
- [ ] Migrar archivos a **Supabase Storage**
- [ ] Usar **Supabase PostgreSQL** para metadatos
- [ ] Desplegar en **Streamlit Community Cloud**

### Fase 3: Mejoras de Funcionalidad
- [ ] Agregar búsqueda/filtrado de audios
- [ ] Guardar transcripciones en BD
- [ ] Historial de transcripciones
- [ ] Exportar transcripciones a PDF/DOCX

### Fase 4: Seguridad y Performance
- [ ] Autenticación de usuarios
- [ ] Encriptación de archivos
- [ ] Cache de transcripciones
- [ ] Optimización de almacenamiento

---

## 10. REQUISITOS DEL SISTEMA

- **Python:** 3.10+
- **RAM:** 4GB mínimo
- **Navegador:** Cualquier navegador moderno
- **Micrófono:** Requerido para grabación
- **Conexión:** Necesaria para APIs de Google/OpenAI

---

## 11. LICENCIA Y CRÉDITOS

**Desarrollado por:** [Tu nombre]  
**Fecha de creación:** Febrero 2026  
**Tecnologías:** Streamlit, Google Generative AI, OpenAI

---

## ANEXO A: Dependencias del Proyecto

```
streamlit==1.31.1
google-generativeai==0.8.6
python-dotenv==1.0.0
openai==1.3.7
```

---

## ANEXO B: Comandos Útiles

```bash
# Ejecutar aplicación
streamlit run index.py

# Ver URL local
streamlit run index.py --logger.level=debug

# Limpiar cache
streamlit cache clear

# Ver configuración
streamlit config show
```

---

**Documento generado:** 5 de Febrero de 2026  
**Versión del informe:** 1.0
