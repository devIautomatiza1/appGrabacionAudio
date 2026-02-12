# 📋 GUÍA DE DEBUGGING: Tickets Auto-Generados

## 🎯 Problema
Los tickets generados automáticamente por IA no aparecen en la sección "Tickets de Oportunidades de Negocio"

## 🔍 Cómo Debuggear

### Paso 1: Ejecuta Streamlit en Terminal
```bash
streamlit run frontend/index.py
```

### Paso 2: Abre la Terminal/Consola donde Corre Streamlit
Deberías ver muchos logs aquí (es normal).

### Paso 3: Transcribe un Audio Nuevo
1. Sube o graba un audio nuevo
2. Selecciónalo en "Selecciona un audio para transcribir"
3. Haz clic en "Transcribir"
4. Espera a que termine

### Paso 4: BUSCA EN LOS LOGS

Busca los siguientes patrones en la consola:

#### 🟢 Si ves esto → ÉXITO
```
========== ANÁLISIS DE IA INICIADO ==========
[STREAMLIT] selected_audio: 'nombre_archivo'
[STREAMLIT] recordings_map keys: ['archivo1', 'archivo2', ...]
[STREAMLIT] recording_id obtenido: <uuid valido>
[STREAMLIT] ✅ Análisis completado
[STREAMLIT] Detectadas: N | Guardadas: N
========== FIN DEL ANÁLISIS ==========

✅ Opp 1 guardada: <id>
✅ Opp 2 guardada: <id>
✅ Opp 3 guardada: <id>
```

**→ Ve a "Tickets de Oportunidades" y deberías verlos**

---

#### 🔴 Si ves esto → PROBLEMA 1: Sin recording en map
```
[STREAMLIT] recordings_map keys: []
[STREAMLIT] recording_id obtenido: None
```
**Causa:** `recordings_map` está vacío
**Solución:** 
- Verifica que Supabase esté configurada correctamente
- Comprueba que haya recordings en tabla `recordings`

---

#### 🔴 Si ves esto → PROBLEMA 2: Nombre no coincide
```
[STREAMLIT] selected_audio: 'ayudar - 2026-02-12T06:58:03.890691'
[STREAMLIT] recordings_map keys: ['ayudar - 2026-02-12T06:58:03.890691.wav']
[STREAMLIT] recording_id obtenido: None
```
**Causa:** El nombre en el mapa tiene `.wav`, pero selected_audio no
**Solución:** Automática (código lo busca por variantes ahora)

---

#### 🔴 Si ves esto → PROBLEMA 3: IA no detectó
```
[STREAMLIT] ✅ Análisis completado
[STREAMLIT] Detectadas: 0 | Guardadas: 0
```
**Causa:** La IA no encontró oportunidades
**Solución:** 
- Verifica la transcripción (tiene palabras clave?)
- Revisa keywords_dict.json (temas configurados?)

---

#### 🔴 Si ves esto → PROBLEMA 4: Detectó pero no guardó
```
[STREAMLIT] ✅ Análisis completado
[STREAMLIT] Detectadas: 5 | Guardadas: 0
[STREAMLIT] Tema 'XXX' NO está en diccionario
```
**Causa:** Gemini devolvió un tema que no existe en keywords_dict.json
**Solución:** Revisa Keywords_dict.json y agrega el tema faltante

---

#### 🔴 Si ves esto → PROBLEMA 5: DB Error
```
[STREAMLIT] Detectadas: 5 | Guardadas: 0
❌ Opp 1: Error <tipo error> - <mensaje>
```
**Causa:** Error al insertar en Supabase
**Solución:** 
- Verifica conexión a Supabase
- Verifica permisos RLS en tabla `opportunities`
- Verifica que la tabla tiene columnas correctas

---

## 📊 Verificación Manual en Supabase

### 1. ¿Existen recordings?
```sql
SELECT filename, id FROM recordings ORDER BY created_at DESC LIMIT 5
```

### 2. ¿Existen opportunities?
```sql
SELECT title, recording_id, created_at FROM opportunities ORDER BY created_at DESC LIMIT 10
```

### 3. ¿Las opportunities tienen recording_id válido?
```sql
SELECT o.id, o.title, o.recording_id, r.filename 
FROM opportunities o
LEFT JOIN recordings r ON o.recording_id = r.id
WHERE o.title LIKE '[IA]%'
ORDER BY o.created_at DESC
LIMIT 10
```

Si ves NULL en `r.filename` → el recording_id no existe en tabla recordings

---

## 🚀 Acciones Rápidas

1. **Vuelve a cargar Streamlit:** `Ctrl+C` en terminal, ejecuta nuevamente
2. **Limpia cache:** `streamlit cache clear`
3. **Revisa logs con más detalle:** Abre DevTools (F12) → Console

---

## ❓ Reporta

Si aún así no funciona, comparte:
1. El FULL log de Streamlit (toda la sección entre `==========`)
2. Resultado del SQL en Supabase (¿existen opportunities con [IA]?)
3. El último error exacto que ves

👨‍💻
