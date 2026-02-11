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
            
            # Prompt inteligente con diarización e identificación deductiva de nombres
            prompt = """Transcribe esta reunión o conversación siguiendo ESTRICTAMENTE estas reglas:

1. **Diarización**: Detecta cada vez que cambia la voz. Identifica quién habla.

2. **Identificación de Nombres** (Efecto Deductivo):
   - Si alguien dice "Hola María, ¿cómo estás?" y otra voz responde, esa voz es María.
   - Si la [Voz 1] dice "Juan, necesito el informe" dirigiéndose a otra voz, esa voz es Juan.
   - Una vez identificado un nombre, úsalo en TODA la transcripción para esa voz.

3. **Formato de salida** (SIN EXPLICACIONES, solo texto):
   Nombre: "Lo que dijo..."
   
   Ejemplo:
   Jorge: "Hola a todos, gracias por venir."
   María: "Gracias Jorge, ¿empezamos con el presupuesto?"
   Voz 3: "Yo aún no tengo el documento."
   
4. **Reglas especiales**:
   - Si no se menciona el nombre, usa "Voz 1", "Voz 2", etc.
   - Mantén coherencia: una voz = UN nombre durante TODA la transcripción.
   - Preserva exactamente lo que dijeron, con puntuación natural.
   - Separa cada intervención en una nueva línea.

Devuelve SOLO la transcripción limpia, sin notas o explicaciones."""
            
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

