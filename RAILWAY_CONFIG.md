# 🚀 Configuración de Railway para iPrevencion

## ✅ Estado Actual

Tu aplicación ya está conectada en Railway con estas variables:

```
RAILWAY_PRIVATE_DOMAIN=appgrabacionaudio.railway.internal
RAILWAY_PROJECT_NAME=sweet-laughter
RAILWAY_ENVIRONMENT_NAME=production
RAILWAY_SERVICE_NAME=appGrabacionAudio
RAILWAY_PROJECT_ID=61fe0cec-83fe-4749-9cee-2fb3a891b44b
RAILWAY_ENVIRONMENT_ID=aaabf712-f493-49e1-9301-c531a23d68a8
RAILWAY_SERVICE_ID=3bed4cc1-2f5e-49a7-a8a0-2eda7a71346b
```

## 🔧 Pasos Requeridos

### 1️⃣ Railway → Environment Variables → Agregar:

```env
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=<genera-con-python>
GEMINI_API_KEY=AIZaSyBY0dDrFECdl_Zou7CqG60QQSTaan1Iyn4
ALLOWED_ORIGINS=http://localhost:8501,https://tu-streamlit-url.streamlit.app
```

**Generar SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2️⃣ Asegurar DATABASE_URL

En Railway → PostgreSQL service:
- Copia el `Database URL`
- Te debe verse así: `postgresql://postgres@appgrabacionaudio.railway.internal:5432/railway`

### 3️⃣ Redeploy Backend

Railway → appGrabacionAudio → Click "Redeploy"

## ⚠️ Errores Comunes

### "GEMINI_API_KEY not found"
- Irá a https://makersuite.google.com/app/apikey
- Copia tu API Key
- Agrega a Railway Environment

### "Connection refused (DATABASE)"
- Usa la URL **privada interna** de Railway:
  ```
  postgresql://postgres@appgrabacionaudio.railway.internal:5432/iprevencion
  ```
- NO uses localhost

### "ModuleNotFoundError"
- En Railway → Settings → Root Directory: `backend/`

## ✅ Verificar que Funciona

```bash
# Testar que el API está vivo
curl https://appgrabacionaudio.railway.app/health

# Ver documentación interactiva
https://appgrabacionaudio.railway.app/docs
```

## 📋 Checklist Final

- [ ] Variables de entorno en Railway ✅
- [ ] DATABASE_URL conecta a PostgreSQL Railway
- [ ] GEMINI_API_KEY configurada  
- [ ] SECRET_KEY generada (NO default)
- [ ] Redeploy iniciado
- [ ] /health endpoint responde
- [ ] /docs accesible

---

**¿Problema?** Revisa logs en Railway:
```
Railway → appGrabacionAudio → Build Logs / Deploy Logs / Runtime Logs
```
