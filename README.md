# Sistema Control Audio - Iprevencion

Sistema inteligente de análisis de audios con IA para gestión de oportunidades de negocio.

## Características

✅ **Grabación de audio** - Graba directamente desde tu micrófono  
✅ **Carga de archivos** - Soporta múltiples formatos (MP3, WAV, M4A, OGG, FLAC, WebM)  
✅ **Transcripción automática** - Usa Google Gemini para transcribir audios  
✅ **Análisis inteligente** - Extrae oportunidades basadas en palabras clave  
✅ **Chat IA** - Realiza preguntas sobre el contenido del audio  
✅ **Gestión en BD** - Almacena grabaciones, transcripciones y oportunidades en Supabase  

## Requisitos previos

- Python 3.8+
- Cuenta en [Google Cloud](https://cloud.google.com) con Gemini API habilitada
- Cuenta en [Supabase](https://supabase.com)

## Instalación

1. **Clonar repositorio**
```bash
git clone <tu_repo>
cd appGrabacionAudio
```

2. **Crear ambiente virtual**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Edita .env y agrega tus credenciales
```

Variables necesarias:
- `GEMINI_API_KEY` - Tu clave de API de Google Gemini
- `SUPABASE_URL` - URL de tu proyecto Supabase
- `SUPABASE_KEY` - Clave anónima de Supabase

5. **Crear base de datos**
Ejecuta el script SQL en tu proyecto Supabase:
```bash
# Copia el contenido de basedatos.sql en el SQL Editor de Supabase
```

## Uso

### Ejecutar la aplicación
```bash
streamlit run streamlit_app.py
```

### Flujo de trabajo

1. **Carga un audio**
   - Graba desde tu micrófono O
   - Sube un archivo de audio

2. **Transcribe**
   - Haz click en "Transcribir"
   - Se guardará automáticamente en Supabase

3. **Agrega palabras clave** (opcional)
   - Define palabras clave importantes
   - Proporciona contexto para cada una

4. **Genera oportunidades**
   - Haz click en "Analizar y Generar Tickets"
   - El sistema extrae oportunidades basadas en palabras clave

5. **Edita y gestiona**
   - Cambia estado y prioridad
   - Agrega notas
   - Guarda cambios

6. **Chat con IA**
   - Realiza preguntas sobre el audio
   - La IA responde basándose en la transcripción

## Estructura del proyecto

```
appGrabacionAudio/
├── frontend/
│   ├── index.py              # Interfaz principal
│   ├── AudioRecorder.py      # Grabación y gestión de audio
│   ├── styles.py             # Estilos CSS
│   ├── notifications.py      # Sistema de notificaciones
│   └── utils.py              # Funciones utilitarias
├── backend/
│   ├── Transcriber.py        # Transcripción con Gemini
│   ├── Model.py              # Chat IA
│   ├── OpportunitiesManager.py  # Extracción de oportunidades
│   └── database.py           # Conexión a Supabase
├── data/
│   ├── recordings/           # Audios grabados
│   └── opportunities/        # Oportunidades locales
├── config.py                 # Configuración centralizada
├── logger.py                 # Sistema de logging
├── streamlit_app.py          # Entry point
├── basedatos.sql             # Schema de BD
└── requirements.txt          # Dependencias
```

## Mejoras realizadas

### 🐛 Correcciones de bugs
- ✅ Corregido bug de caché en Transcriber que reutilizaba transcripciones
- ✅ Eliminado código duplicado en carga de archivos (grabación y upload)

### 🔧 Mejoras de arquitectura
- ✅ Creado `config.py` para centralizar configuración
- ✅ Implementado sistema de logging (`logger.py`)
- ✅ Creado `.env.example` para facilitar setup
- ✅ Agregadas funciones utilitarias reutilizables (`utils.py`)

### 🛡️ Validaciones y seguridad
- ✅ Validación de tamaño máximo de archivo (100MB)
- ✅ Validación de extensiones de archivo
- ✅ Mejor manejo de excepciones específicas
- ✅ Logging de todas las operaciones

### 📚 Documentación
- ✅ Docstrings en todas las funciones
- ✅ Comentarios explicativos en el código
- ✅ README completo con instrucciones

## Limitaciones actuales

- Máximo 100MB por archivo de audio
- Requiere conexión a Internet para transcripción y IA
- Gemini tiene límites de rate limiting según plan

## Troubleshooting

### Error de conexión a Supabase
```
"No se pudo conectar a Supabase"
```
**Solución:**
1. Verifica que SUPABASE_URL y SUPABASE_KEY estén correctos en `.env`
2. Asegúrate de que RLS esté DESHABILITADO en todas las tablas
3. Intenta: Menú (3 puntos) → "Reboot app"

### Error al transcribir
```
"GEMINI_API_KEY no está configurada"
```
**Solución:**
1. Obtén tu clave en [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Agrega la clave a tu `.env`
3. Reinicia la aplicación

### Archivo demasiado grande
```
"Archivo demasiado grande (X.XMB). Máximo: 100MB"
```
**Solución:**
- Comprime el archivo de audio
- Usa un formato de menor tamaño
- Divide el audio en segmentos más pequeños

## Logs

Los logs se guardan en `data/app.log`. Revísalos para debuggear problemas:
```bash
tail -f data/app.log
```

## Contribuir

Las mejoras y reportes de bugs son bienvenidos. Por favor:
1. Crea un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo licencia MIT.

## Soporte

Para soporte, contacta al equipo de desarrollo de Iprevencion.

---

**Versión:** 1.0.0  
**Última actualización:** 2026-02-09
