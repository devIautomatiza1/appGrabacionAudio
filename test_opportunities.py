#!/usr/bin/env python
"""Test script para verificar análisis de oportunidades"""
import sys
import json
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from OpportunitiesManager import OpportunitiesManager
from logger import get_logger

logger = get_logger(__name__)

# Transcripción de prueba
test_transcription = """Jaime: "Buenos, buenos días a todos. Hoy necesitamos hablar del presupuesto para este trimestre. Estimamos que necesitamos unos $75,000 para invertir en nuevas herramientas en software. ¿Todos de acuerdo?"
Mónica: "Sí, estoy de acuerdo con Jaime, pero alguien tiene que contactar a los proveedores para negociar los precios. Yo no tengo tiempo esta semana. ¿Quién se puede encargar?"
Fran: "Yo me encargo de eso Mónica. También hemos considerado los temas de compliance. Necesitamos asegurarnos de que cumplimos todas las regulaciones antes de implementar nada nuevo."
Jaime: "Excelente pregunta, Fran. Vamos a necesitar entrenar al equipo en esta nueva plataforma. ¿Podríamos contratar a alguien especializado para dar los cursos?"
Mónica: "Buena idea y otra cosa, tenemos un cliente grande interesado en nuestros servicios. Creo que es el momento perfecto para cerrar ese deal. ¿Alguien puede trabajar en la propuesta esta semana?"
Fran: "Yo puedo ayudar con eso, pero primero necesitamos resolver lo del presupuesto y contactar ese proveedor. Eso es de acción inmediata."
Jaime: "Perfecto. Entonces, Fran contacta a proveedores, alguien trabaja en la propuesta del cliente y buscamos a alguien para la capacitación. ¿Estáis listos?"
Mónica: "Sí."
"""

def test_gemini_analysis():
    """Test el analisis directo sin BD"""
    import google.generativeai as genai
    from config import GEMINI_API_KEY
    
    # Configurar Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Diccionario de temas
    temas = {
        "Presupuesto": {"prioridad": "high"},
        "Formación": {"prioridad": "medium"},
        "Cierre de venta": {"prioridad": "high"},
        "Decisión importante": {"prioridad": "high"},
        "Infraestructura": {"prioridad": "medium"},
        "Recursos Humanos": {"prioridad": "medium"},
        "Cumplimiento Legal": {"prioridad": "high"},
        "Acción requerida": {"prioridad": "high"},
    }
    
    speakers_list = "Jaime, Mónica, Fran"
    
    prompt = f"""CRÍTICO: Analiza esta conversación/reunión palabra por palabra. Detecta TODAS las oportunidades que encuentres.

MAPEO SIMPLE:
• Presupuesto / dinero / gasto / inversión / coste → "Presupuesto" (HIGH)
• Contactar / llamar / tarea / acción / hacer / pendiente / debe / responsabilidad → "Acción requerida" (HIGH)
• Regulación / ley / cumplimiento / compliance / auditoría / riesgo legal → "Cumplimiento Legal" (HIGH)
• Formación / capacitación / entrenamiento / curso / educación → "Formación" (MEDIUM)
• Contratar / empleado / personal / equipo / rol / recurso humano → "Recursos Humanos" (MEDIUM)
• Cliente / venta / deal / contrato / negocio / oportunidad / acuerdo → "Cierre de venta" (HIGH)
• Decisión / cambio / estrategia / importante / aprobado → "Decisión importante" (HIGH)
• Herramienta / infraestructura / sistema / plataforma / equipo tecnológico → "Infraestructura" (MEDIUM)

TRANSCRIPCIÓN:
{test_transcription}

SPEAKERS: {speakers_list}

RESPONDE SOLO CON JSON (sin markdown, sin explicaciones):

{{"analisis_completo": true, "oportunidades": [{{"tema": "TemaExacto", "prioridad": "high/medium/low", "mencionado_por": "Nombre", "contexto": "frase", "confianza": 0.85}}]}}

Si no hay oportunidades: {{"analisis_completo": true, "oportunidades": []}}"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    response_text = response.text.strip()
    
    print("\n[RESPUESTA GEMINI] (raw):")
    print("-" * 80)
    print(response_text[:500])
    print("-" * 80)
    
    # Limpiar y parsear
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0].strip()
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0].strip()
    
    try:
        response_json = json.loads(response_text)
        oportunidades = response_json.get("oportunidades", [])
        
        print(f"\n[OK] JSON PARSEADO: {len(oportunidades)} oportunidades detectadas")
        print("\n[DETALLES]:")
        for i, opp in enumerate(oportunidades, 1):
            print(f"\n   {i}. {opp.get('tema')} ({opp.get('prioridad').upper()})")
            print(f"      Por: {opp.get('mencionado_por')}")
            print(f"      Contexto: {opp.get('contexto')[:80]}...")
            print(f"      Confianza: {opp.get('confianza'):.0%}")
        
        return len(oportunidades), oportunidades
        
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] Error parsing JSON: {str(e)}")
        print(f"Text: {response_text[:200]}")
        return 0, []

def main():
    print("=" * 80)
    print("TEST: Analisis de Oportunidades con IA (MODO GEMINI DIRECTO)")
    print("=" * 80)
    
    try:
        num_opps, opps_list = test_gemini_analysis()
        print(f"\n\n{'=' * 80}")
        print(f"RESULTADO FINAL: {num_opps} oportunidades detectadas por Gemini [OK]")
        print(f"{'=' * 80}\n")
        
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__} - {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

