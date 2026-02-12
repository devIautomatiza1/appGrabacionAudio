"""Test completo del flujo de detección y guardado"""
import sys
from pathlib import Path

# Añadir backend al path para importar OpportunitiesManager
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from OpportunitiesManager import OpportunitiesManager
from logger import get_logger

logger = get_logger(__name__)

# Transcripción de ejemplo (con formato de hablantes)
test_transcription = """
Jaime: Hola, necesitamos un presupuesto nuevo para el proyecto de infraestructura.
Mónica: Exacto, estamos gastando mucho en recursos y hay que optimizar.
Fran: Además, hay cumplimiento legal que debemos revisar antes de implementar cualquier cosa.
Jaime: Sí, y queremos formar al equipo en las nuevas tecnologías.
Mónica: También necesitamos tomar una decisión importante sobre el cierre de este proyecto.
Fran: No olvidemos que hay acciones requeridas del último cliente.
Jaime: Claro, eso afecta los recursos humanos también.
"""

filename = "test_audio_2024.wav"

print("\n" + "="*60)
print("TEST: Detección y Guardado de Oportunidades")
print("="*60)

manager = OpportunitiesManager()
print(f"\n[INFO] OpportunitiesManager inicializado")
print(f"[INFO] DB disponible: {manager.db is not None}")

print(f"\n[PASO 1] Analizando transcripción...")
detected, saved = manager.analyze_opportunities_with_ai(test_transcription, filename)

print(f"\n[RESULTADO]")
print(f"  - Detectadas: {detected}")
print(f"  - Guardadas: {len(saved)}")
if saved:
    print(f"\n[DETALLES DE GUARDADAS]")
    for i, opp in enumerate(saved, 1):
        print(f"  {i}. {opp.get('title')}")
        print(f"     ID: {opp.get('id')}")
        print(f"     Priority: {opp.get('priority')}")
else:
    print(f"  ⚠️  No se guardaron oportunidades")

print("\n" + "="*60)
print("✅ Test completado" if saved else f"⚠️  Se detectaron {detected} pero no se guardaron")
print("="*60 + "\n")
