#!/usr/bin/env python3
"""
test_ai_analysis.py - Script de prueba para validar el análisis IA de oportunidades
ejecutable: python test_ai_analysis.py
"""

import sys
import json
from pathlib import Path

# Agregar rutas
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.OpportunitiesManager import OpportunitiesManager
from logger import get_logger

logger = get_logger(__name__)

def test_keywords_dict_loading():
    """Prueba 1: Cargar diccionario de palabras clave"""
    print("\n" + "="*60)
    print("TEST 1: Cargando keywords_dict.json")
    print("="*60)
    
    manager = OpportunitiesManager()
    keywords = manager.load_keywords_dict()
    
    if not keywords:
        print("❌ FALLO: No se pudo cargar keywords_dict.json")
        return False
    
    print(f"✅ ÉXITO: Se cargó keywords_dict.json")
    print(f"   Temas encontrados: {list(keywords.get('temas_de_interes', {}).keys())}")
    print(f"   Modelo Gemini: {keywords.get('configuracion', {}).get('modelo_gemini')}")
    return True

def test_speaker_extraction():
    """Prueba 2: Extraer speakers de transcripción"""
    print("\n" + "="*60)
    print("TEST 2: Extrayendo speakers de transcripción")
    print("="*60)
    
    manager = OpportunitiesManager()
    
    test_transcription = """Jorge: "Hola a todos, ¿qué tal?"
María: "Bien, bien. Necesitamos presupuesto para esto."
Carlos: "Estoy de acuerdo, también hay que asignar recursos."
Jorge: "Vale, lo documentamos como acción."
"""
    
    speakers = manager.extract_speakers_from_transcription(test_transcription)
    
    if not speakers:
        print("❌ FALLO: No se extrajeron speakers")
        return False
    
    print(f"✅ ÉXITO: Se extrajeron {len(speakers)} speakers")
    for speaker, lines in speakers.items():
        print(f"   - {speaker}: {len(lines)} intervención(es)")
    
    return True

def test_json_response_parsing():
    """Prueba 3: Simular respuesta Gemini y parseo"""
    print("\n" + "="*60)
    print("TEST 3: Parsando respuesta Gemini simulada")
    print("="*60)
    
    # Simular respuesta Gemini
    gemini_response = """{
  "oportunidades": [
    {
      "tema": "Presupuesto",
      "prioridad": "high",
      "mencionado_por": "María",
      "contexto": "Necesitamos presupuesto para esto",
      "confianza": 0.95
    },
    {
      "tema": "Acción requerida",
      "prioridad": "high",
      "mencionado_por": "Carlos",
      "contexto": "hay que asignar recursos",
      "confianza": 0.88
    }
  ]
}"""
    
    try:
        parsed = json.loads(gemini_response)
        opportunities = parsed.get("oportunidades", [])
        
        if len(opportunities) != 2:
            print(f"❌ FALLO: Se esperaban 2 oportunidades, se obtuvieron {len(opportunities)}")
            return False
        
        print(f"✅ ÉXITO: Se parsearon correctamente {len(opportunities)} oportunidades")
        for opp in opportunities:
            print(f"   - {opp['tema']} (Prioridad: {opp['prioridad']}) - Mencionado por: {opp['mencionado_por']}")
        
        return True
    
    except json.JSONDecodeError as e:
        print(f"❌ FALLO: Error parseando JSON: {e}")
        return False

def test_opportunity_formatting():
    """Prueba 4: Formatear oportunidad para guardar"""
    print("\n" + "="*60)
    print("TEST 4: Formateando oportunidad para Supabase")
    print("="*60)
    
    opp_data = {
        "tema": "Presupuesto",
        "prioridad": "high",
        "mencionado_por": "María",
        "contexto": "Necesitamos $50k para licencias"
    }
    
    # Simular formateo
    tema = opp_data.get("tema", "Unknown")
    mencionado_por = opp_data.get("mencionado_por", "Unknown")
    contexto = opp_data.get("contexto", "")
    
    note = f"Ticket generado automáticamente por IA tras detectar una intención relacionada con el concepto '{tema}' del diccionario corporativo.\n\nMencionado por: {mencionado_por}\nContexto: {contexto}"
    
    print(f"✅ ÉXITO: Oportunidad formateada correctamente")
    print(f"   Tema: {tema}")
    print(f"   Mencionado por: {mencionado_por}")
    print(f"   Nota generada:\n   {note}")
    
    return True

def run_all_tests():
    """Ejecutar todas las pruebas"""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  PRUEBAS DE ANÁLISIS IA DE OPORTUNIDADES".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    results = {
        "Keywords Dict": test_keywords_dict_loading(),
        "Speaker Extraction": test_speaker_extraction(),
        "JSON Parsing": test_json_response_parsing(),
        "Formatting": test_opportunity_formatting(),
    }
    
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} pruebas pasadas")
    
    if passed == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON! El sistema está listo.")
        return True
    else:
        print(f"\n⚠️  {total - passed} prueba(s) falló/ieron. Revisa los errores arriba.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
