"""Diagnóstico: Verificar flujo completo"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from OpportunitiesManager import OpportunitiesManager
from database import init_supabase
from logger import get_logger

logger = get_logger(__name__)

print("\n" + "="*70)
print("DIAGNÓSTICO: Flujo de Guardado de Oportunidades")
print("="*70)

# 1. Verificar BD disponible
db = init_supabase()
print(f"\n1️⃣ Supabase disponible: {db is not None}")

if db:
    # 2. Ver recordings en BD
    print(f"\n2️⃣ Recordings en BD:")
    try:
        result = db.table("recordings").select("id, filename, created_at").order("created_at", desc=True).limit(5).execute()
        if result.data:
            for rec in result.data:
                print(f"   - {rec['filename']} (ID: {rec['id'][:8]}...)")
        else:
            print(f"   ⚠️  Sin recordings")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. Ver opportunities en BD
    print(f"\n3️⃣ Opportunities en BD:")
    try:
        result = db.table("opportunities").select("id, title, recording_id, created_at").order("created_at", desc=True).limit(5).execute()
        if result.data:
            for opp in result.data:
                print(f"   - {opp['title'][:50]}")
                print(f"     Recording ID: {opp.get('recording_id', 'None')}")
        else:
            print(f"   ⚠️  Sin opportunities")
    except Exception as e:
        print(f"   ❌ Error: {e}")

# 4. Test: Simular análisis
print(f"\n4️⃣ Test análisis:")
print("="*70)

test_filename = "ayudar - 2026-02-12T06:58:03.890691.wav"
test_transcription = """
Jaime: Hola, necesitamos un presupuesto para el proyecto.
Mónica: Exacto, hay que revisar el cumplimiento legal también.
"""

manager = OpportunitiesManager()
print(f"\nArchivo de prueba: {test_filename}")
print(f"Transcripción: {test_transcription[:50]}...")

# Ver si existe el recording
if db:
    print(f"\n  Buscando en BD: {test_filename}")
    result = db.table("recordings").select("id").eq("filename", test_filename).execute()
    if result.data:
        print(f"  ✅ Encontrado: {result.data[0]['id']}")
    else:
        print(f"  ❌ No encontrado")
        print(f"\n  Probando variantes:")
        for variant in [test_filename.replace(".wav", ""), 
                      test_filename.replace(" ", "_"),
                      test_filename.replace("_", " ")]:
            result = db.table("recordings").select("id").eq("filename", variant).execute()
            if result.data:
                print(f"     ✅ Encontrada variante: '{variant}'")
            else:
                print(f"     ❌ '{variant}'")

# Test análisis
print(f"\nEjecutando análisis...")
detected, saved = manager.analyze_opportunities_with_ai(test_transcription, test_filename)

print(f"\n📊 Resultado:")
print(f"   Detectadas: {detected}")
print(f"   Guardadas: {len(saved)}")

if saved:
    print(f"\n✅ Oportunidades guardadas:")
    for opp in saved:
        print(f"   - {opp['title']}")
else:
    print(f"   ⚠️  No se guardaron")

print("\n" + "="*70 + "\n")
