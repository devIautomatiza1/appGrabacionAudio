"""
Test para verificar la extracción de audios desde Supabase
"""
import sys
import os
from pathlib import Path
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from supabase import create_client
except ImportError:
    print("❌ Supabase no está instalado")
    print("Instala con: pip install supabase")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("❌ python-dotenv no está instalado") 
    print("Instala con: pip install python-dotenv")
    sys.exit(1)

# Cargar variables de entorno
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("=" * 60)
print("TEST: Extrayendo audios de Supabase")
print("=" * 60)

# Verificar credenciales
print(f"\n1. Verificando credenciales:")
print(f"   URL: {SUPABASE_URL[:50] if SUPABASE_URL else 'NO ENCONTRADA'}...")
print(f"   KEY: {SUPABASE_KEY[:30] if SUPABASE_KEY else 'NO ENCONTRADA'}...")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("\n❌ ERROR: Falta SUPABASE_URL o SUPABASE_KEY en .env")
    sys.exit(1)

# Conectarse a Supabase
print(f"\n2. Conectando a Supabase...")
try:
    supabase = create_client(SUPABASE_URL.strip(), SUPABASE_KEY.strip())
    print("   ✅ Conexión exitosa")
except Exception as e:
    print(f"   ❌ Error de conexión: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Obtener todos los registros
print(f"\n3. Obteniendo tabla 'recordings'...")
try:
    response = supabase.table("recordings").select("*").execute()
    print(f"   ✅ Query ejecutada")
    
    if response.data:
        print(f"\n   📊 Total de audios encontrados: {len(response.data)}")
        print(f"\n   Detalles de cada audio:")
        for i, record in enumerate(response.data, 1):
            print(f"\n   Audio #{i}:")
            for key, value in record.items():
                print(f"     - {key}: {value}")
    else:
        print("\n   ⚠️  No hay audios en la tabla")
        
except Exception as e:
    print(f"   ❌ Error obteniendo registros: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Prueba con query específico (como en AudioRecorder)
print(f"\n4. Obteniendo audios (solo filenames) ordenados por fecha DESC...")
try:
    response = supabase.table("recordings").select("filename").order("created_at", desc=True).execute()
    
    if response.data:
        filenames = [record["filename"] for record in response.data]
        print(f"   ✅ Filenames obtenidos: {filenames}")
        print(f"\n   Array que retorna la función: {filenames}")
    else:
        print(f"   ⚠️ Sin datos")
        
except Exception as e:
    print(f"   ❌ Error con query específico: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETADO")
print("=" * 60)
