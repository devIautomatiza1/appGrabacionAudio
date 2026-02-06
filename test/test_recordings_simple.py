"""
Test simple para diagnosticar el problema con la lectura de audios desde Supabase
"""
import os
import sys
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("=" * 70)
print("TEST SIMPLE: Diagnóstico de la extracción de audios desde Supabase")
print("=" * 70)

# Paso 1: Verificar credenciales
print("\n[1] Verificando credenciales en .env:")
if SUPABASE_URL:
    print(f"    ✅ SUPABASE_URL encontrada: {SUPABASE_URL[:40]}...")
else:
    print("    ❌ SUPABASE_URL NO encontrada")
    sys.exit(1)

if SUPABASE_KEY:
    print(f"    ✅ SUPABASE_KEY encontrada: {SUPABASE_KEY[:30]}...")
else:
    print("    ❌ SUPABASE_KEY NO encontrada")
    sys.exit(1)

# Paso 2: Intentar importar y usar supabase
print("\n[2] Importando supabase...")
try:
    from supabase import create_client
    print("    ✅ Supabase importado correctamente")
except ImportError as e:
    print(f"    ❌ Error importando supabase: {e}")
    print("\n    💡 Solución: Instala con: pip install supabase")
    sys.exit(1)

# Paso 3: Conectarse
print("\n[3] Conectando a Supabase...")
try:
    client = create_client(SUPABASE_URL.strip(), SUPABASE_KEY.strip())
    print("    ✅ Conexión exitosa")
except Exception as e:
    print(f"    ❌ Error de conexión: {e}")
    sys.exit(1)

# Paso 4: Query a la tabla recordings
print("\n[4] Ejecutando SELECT * FROM recordings...")
try:
    response = client.table("recordings").select("*").execute()
    print(f"    ✅ Query ejecutada")
    print(f"    - Respuesta: {response}")
    
    if hasattr(response, 'data') and response.data:
        print(f"\n    📊 DATOS ENCONTRADOS:")
        print(f"       Total de audios: {len(response.data)}")
        for idx, record in enumerate(response.data, 1):
            print(f"\n       Audio #{idx}:")
            for key, value in record.items():
                print(f"         • {key}: {value}")
    else:
        print("    ⚠️ Sin datos en la tabla")
        print(f"    - response.data = {response.data if hasattr(response, 'data') else 'NO TIENE ATRIBUTO data'}")
        
except Exception as e:
    print(f"    ❌ Error en query: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Paso 5: Query solo filenames (como en AudioRecorder.get_recordings_from_supabase)
print("\n[5] Ejecutando SELECT filename FROM recordings ORDER BY created_at DESC...")
try:
    response = client.table("recordings").select("filename").order("created_at", desc=True).execute()
    print(f"    ✅ Query ejecutada")
    
    if hasattr(response, 'data') and response.data:
        filenames = [record["filename"] for record in response.data]
        print(f"    ✅ Filenames obtenidos: {filenames}")
        print(f"\n    🎯 Array que retornaría la función:")
        print(f"       {filenames}")
    else:
        print(f"    ❌ Sin datos retornados")
        
except Exception as e:
    print(f"    ❌ Error en query: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ TEST COMPLETADO - TODO FUNCIONA CORRECTAMENTE")
print("=" * 70)
