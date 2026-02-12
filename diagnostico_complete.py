"""Diagnóstico completo del problema de guardado"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from OpportunitiesManager import OpportunitiesManager
from database import init_supabase
from logger import get_logger
import json

logger = get_logger(__name__)

print("\n" + "="*80)
print("DIAGNÓSTICO COMPLETO: Por qué no se guardan los tickets")
print("="*80)

db = init_supabase()
print(f"\n1️⃣ Supabase disponible: {db is not None}")

if not db:
    print("❌ No hay conexión a Supabase, prueba local no es posible")
    sys.exit(1)

# Verificar tabla recordings
print(f"\n2️⃣ Verificar tabla recordings:")
try:
    result = db.table("recordings").select("id, filename").order("created_at", desc=True).limit(3).execute()
    if result.data:
        for rec in result.data:
            print(f"   ID: {rec['id'][:8]}... | Filename: {rec['filename']}")
            recordings_data = rec
    else:
        print("   ⚠️  Sin recordings")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Tomar el último recording para prueba
recording_id = recordings_data['id']
filename = recordings_data['filename']

print(f"\n3️⃣ Usar para prueba:")
print(f"   Recording ID: {recording_id}")
print(f"   Filename: {filename}")

# Test transcripción simple
test_transcription = """
Jaime: Necesitamos un presupuesto nuevo
Mónica: También hay que revisar el cumplimiento legal
"""

print(f"\n4️⃣ Ejecutar análisis con recording_id pasado directamente:")
print("="*80)

manager = OpportunitiesManager()
print(f"Enviando:")
print(f"  - transcription: {test_transcription[:40]}...")
print(f"  - audio_filename: {filename}")
print(f"  - recording_id: {recording_id}")

detected, saved = manager.analyze_opportunities_with_ai(
    transcription=test_transcription,
    audio_filename=filename,
    recording_id=recording_id
)

print(f"\n📊 Resultado:")
print(f"   Detectadas: {detected}")
print(f"   Guardadas: {len(saved)}")

if saved:
    print(f"\n✅ ÉXITO - Oportunidades guardadas:")
    for opp in saved:
        print(f"   - ID: {opp.get('id')}")
        print(f"     Title: {opp.get('title')}")
        print(f"     Recording ID: {opp.get('recording_id')}")
else:
    print(f"\n❌ FALLO - No se guardaron")
    print(f"\nVerificando tabla opportunities:")
    result = db.table("opportunities").select("id, title, recording_id, created_at").order("created_at", desc=True).limit(5).execute()
    if result.data:
        print(f"   Últimas 5 opportunities:")
        for opp in result.data:
            print(f"   - {opp['title'][:40]}")
            print(f"     Recording ID: {opp.get('recording_id')}")
    else:
        print(f"   ⚠️  Tabla vacía")

print("\n" + "="*80 + "\n")
