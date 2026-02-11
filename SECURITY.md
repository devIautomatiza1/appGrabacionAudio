# 🔐 SEGURIDAD - Guía de Implementación

Este documento explica las mejoras de seguridad implementadas en el proyecto.

## 📋 Cambios Realizados

### 1. **Rate Limiting para APIs**

Se ha implementado un sistema de control de velocidad para limitar las llamadas a Google Gemini API.

#### Archivos nuevos:
- `backend/rate_limiter.py` - Módulos `RateLimiter` y `TokenBucketLimiter`

#### Cómo funciona:

**RateLimiter (Cuenta de llamadas):**
```python
from backend.rate_limiter import gemini_limiter

# Verifica si se permite una nueva llamada
if not gemini_limiter.is_allowed("transcription"):
    wait_time = gemini_limiter.get_wait_time("transcription")
    print(f"Espera {wait_time}s")
else:
    # Proceder con la llamada a API
    transcribe_audio()
```

**TokenBucketLimiter (Algoritmo bucket de tokens):**
- Más flexible que rate limiter
- Permite ráfagas mientras mantiene límite general
- Ejemplo: 10 llamadas/minuto pero que puedas usar todas de golpe

#### Variables de entorno (en `.env`):

```env
# Máximo de llamadas a Gemini API por ventana
RATE_LIMIT_CALLS=10

# Ventana de tiempo en segundos
RATE_LIMIT_WINDOW=60

# Tokens en el bucket
RATE_LIMIT_TOKENS=100
```

**Ejemplo de configuración recomendada:**
- Desarrollo: `RATE_LIMIT_CALLS=50, RATE_LIMIT_WINDOW=3600` (50 llamadas/hora)
- Producción: `RATE_LIMIT_CALLS=100, RATE_LIMIT_WINDOW=86400` (100 llamadas/día)

---

### 2. **Validación Robusta de Entrada**

Se ha implementado un validador centralizado para todos los inputs del usuario.

#### Archivo nuevo:
- `backend/input_validator.py` - Clase `InputValidator`

#### Validaciones disponibles:

```python
from backend.input_validator import validator

# Validar nombre de archivo
valid, error = validator.validate_filename("meeting_2025.mp3")
if not valid:
    print(f"Error: {error}")

# Validar palabra clave
valid, error = validator.validate_keyword("oportunidad")

# Validar búsqueda
valid, error = validator.validate_search_query("cliente importante")

# Validar transcripción
valid, error = validator.validate_transcription_text("Este es un texto...")

# Validar tamaño de audio
valid, error = validator.validate_audio_size(size_bytes, max_mb=100)

# Sanitizar strings
clean_text = validator.sanitize_string(user_input)
```

#### Variables de entorno (en `.env`):

```env
# Longitud máxima de nombre de archivo
MAX_FILENAME_LENGTH=255

# Longitud máxima de palabra clave
MAX_KEYWORD_LENGTH=100

# Longitud máxima de búsqueda
MAX_SEARCH_LENGTH=200

# Longitud máxima de transcripción
MAX_TEXT_LENGTH=5000
```

#### Patrones permitidos:

- **Filenames**: Solo caracteres alfanuméricos, guiones, puntos y espacios
- **Keywords**: Letras, números, espacios, guiones y caracteres acentuados (1-100 chars)
- **Text**: Letras, números, espacios, puntos, comas, signos de exclamación, acentos

#### Caracteres/strings bloqueados:

- Rutas relativas: `../`, `..\\`
- Archivos del sistema: `etc/passwd`, `system32`
- Scripts: `<script>`, `<iframe>`, `javascript:`, `onclick:`, `onerror:`

---

### 3. **Integración en el código**

#### Model.py (Chat con Gemini):
```python
from rate_limiter import gemini_limiter
from input_validator import validator

# Valida pregunta y contexto
valid, error = validator.validate_transcription_text(context)
if not valid:
    raise ValueError(f"Contexto inválido: {error}")

# Verifica rate limit
if not gemini_limiter.is_allowed("chat"):
    raise RuntimeError("Límite de API excedido")

# Procede con la llamada
response = self.model.generate_content(prompt)
```

#### Transcriber.py (Transcripción de audio):
```python
# Valida nombre de archivo
valid, error = validator.validate_filename(filename)
if not valid:
    raise ValueError(f"Nombre inválido: {error}")

# Valida tamaño
valid, error = validator.validate_audio_size(file_size_bytes)
if not valid:
    raise ValueError(f"Tamaño inválido: {error}")

# Verifica rate limit
if not gemini_limiter.is_allowed("transcription"):
    raise RuntimeError("Límite de API excedido")
```

#### frontend/utils.py (Procesamiento de audio):
```python
from input_validator import validator

# Valida filename y tamaño
valid, error = validator.validate_filename(filename)
if not valid:
    show_error(f"Nombre inválido: {error}")
    return False, None

valid, error = validator.validate_audio_size(len(audio_bytes))
if not valid:
    show_error(f"Tamaño inválido: {error}")
    return False, None
```

#### frontend/index.py (búsqueda de audios):
```python
from input_validator import validator

# Valida búsqueda
valid, error = validator.validate_search_query(search_query)
if not valid:
    show_error(f"Búsqueda inválida: {error}")
```

---

## 🛡️ Configuración de seguridad recomendada

### Desarrollo:
```env
RATE_LIMIT_CALLS=50
RATE_LIMIT_WINDOW=3600
RATE_LIMIT_TOKENS=100
MAX_AUDIO_SIZE_MB=500
LOG_LEVEL=DEBUG
```

### Producción:
```env
RATE_LIMIT_CALLS=100
RATE_LIMIT_WINDOW=86400
RATE_LIMIT_TOKENS=50
MAX_AUDIO_SIZE_MB=100
LOG_LEVEL=INFO
```

---

## ⚠️ Manejo de errores

El sistema genera diferentes tipos de errores según el problema:

```python
try:
    transcriber.transcript_audio("audio.mp3")
except FileNotFoundError:
    # El archivo no existe
    pass
except ValueError as e:
    # Validación falló (nombre, tamaño, formato)
    print(f"Validación: {e}")
except RuntimeError as e:
    # Rate limit excedido
    print(f"Rate limit: {e}")
except Exception as e:
    # Otros errores
    print(f"Error: {e}")
```

---

## 📊 Monitoreo

Los validadores registran TODO en los logs:

```bash
# Ver logs
tail -f data/app.log

# Ejemplos de logs:
# ✓ Filename validado: recording_20250211_120000.wav
# ✓ Keyword validado: oportunidad
# ⚠️ Rate limit excedido para chat. Espera 15.3s
# ⚠️ Tokens insuficientes para transcription. Disponibles: 0.5, Requeridos: 1
```

---

## 🔄 Próximas mejoras

1. **Autenticación de usuarios** - Implementar login para límites por usuario
2. **Base de datos de límites** - Persistir contadores entre sesiones
3. **Alertas de seguridad** - Notificar sobre intentos sospechosos
4. **Auditoría completa** - Registrar todas las operaciones sensibles
5. **CORS y CSP** - Headers de seguridad en respuestas HTTP

---

## 📚 Referencias

- [OWASP Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [Rate Limiting Best Practices](https://cloud.google.com/architecture/rate-limiting-strategies-techniques)
- [Token Bucket Algorithm](https://en.wikipedia.org/wiki/Token_bucket)

