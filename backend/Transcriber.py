"""Transcriber.py - Transcribidor de audio con Gemini (~45 líneas)"""
import google.generativeai as genai
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_API_KEY, TRANSCRIPTION_MODEL, MIME_TYPES
from logger import get_logger

logger = get_logger(__name__)
genai.configure(api_key=GEMINI_API_KEY)

class Transcriber:
    def __init__(self):
        self.model = genai.GenerativeModel(TRANSCRIPTION_MODEL)
        logger.info("✓ Transcriber initialized")
    
    def transcript_audio(self, audio_path: str):
        """Transcribe un archivo de audio con diarización e identificación de voces"""
        try:
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Archivo no encontrado: {audio_path}")
            
            ext = audio_path.lower().split('.')[-1]
            mime_type = MIME_TYPES.get(ext, 'audio/mpeg')
            
            logger.info(f"Transcribiendo: {audio_path} ({mime_type})")
            audio_file = genai.upload_file(audio_path, mime_type=mime_type)
            
            # Prompt ESTRICTO para diarización completa e identificación de nombres
            prompt = """INSTRUCCIONES CRÍTICAS - DEBES SEGUIRLAS AL PIE DE LA LETRA:

TAREA: Transcribe esta conversación/reunión identificando CADA HABLANTE por separado.

PASO 1 - DETECTAR CAMBIOS DE VOZ:
- Analiza atentamente CADA cambio de voz/hablante
- Marca donde empieza y termina cada intervención
- Si hay 2 voces, habrá 2 hablantes. Si hay 3, habrá 3 hablantes. Etc.

PASO 2 - IDENTIFICAR NOMBRES (EFECTO DEDUCTIVO):
- Si alguien dice "Hola Carlos, ¿qué tal?" → Carlos es el otro hablante
- Si dice "Juan, necesito..." → Juan está siendo mencionado
- Si la Voz 2 dice un nombre dirigiéndose a otra voz → esa voz es ese nombre
- Usa SOLO nombres mencionados en la conversación
- Si no hay nombre mencionado, usa "Voz 1", "Voz 2", etc.

PASO 3 - FORMATO EXACTO (SIN EXCEPCIONES):
CADA INTERVENCIÓN en una NUEVA LÍNEA con este formato:
Nombre: "Lo que dijo exactamente..."

EJEMPLO CORRECTO:
Jorge: "Bueno, ¿qué tal? ¿Cómo estáis?"
María: "Bien, bien. ¿Y tú?"
Voz 3: "Todo correct."

PASO 4 - REGLAS DE ORO:
✓ SEPARA por hablante - cada uno su línea
✓ MANTÉN consistencia - Jorge es Jorge SIEMPRE
✓ PRESERVA exactitud - transcribe word-by-word
✓ SIN EXPLICACIONES - solo el diálogo

SALIDA FINAL: Solo el texto formateado, nada más."""
            
            response = self.model.generate_content([prompt, audio_file])
            
            logger.info(f"✓ Transcripción: {len(response.text)} caracteres")
            
            class Result:
                def __init__(self, text):
                    self.text = text
            
            return Result(response.text)
        
        except FileNotFoundError as e:
            logger.error(f"Archivo no encontrado: {audio_path}")
            raise
        
        except Exception as e:
            logger.error(f"transcript_audio: {type(e).__name__} - {str(e)}")
            raise

