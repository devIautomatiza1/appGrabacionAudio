"""Transcriber.py - Transcribidor de audio con Gemini y rate limiting"""
import google.generativeai as genai
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_API_KEY, TRANSCRIPTION_MODEL, MIME_TYPES, MAX_AUDIO_SIZE_MB
from logger import get_logger
from rate_limiter import gemini_limiter
from input_validator import validator

logger = get_logger(__name__)
genai.configure(api_key=GEMINI_API_KEY)

class Transcriber:
    def __init__(self):
        self.model = genai.GenerativeModel(TRANSCRIPTION_MODEL)
        logger.info("✓ Transcriber initialized")
    
    def transcript_audio(self, audio_path: str):
        """Transcribe un archivo de audio con validación y rate limiting
        
        Args:
            audio_path: Ruta del archivo de audio
            
        Returns:
            Objeto con atributo 'text' conteniendo la transcripción
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si es inválido
            RuntimeError: Si se excede rate limit
        """
        try:
            # ===== VALIDACIÓN DE RUTA Y ARCHIVO =====
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Archivo no encontrado: {audio_path}")
            
            filename = os.path.basename(audio_path)
            valid, error = validator.validate_filename(filename)
            if not valid:
                raise ValueError(f"Nombre de archivo inválido: {error}")
            
            # ===== VALIDACIÓN DE TAMAÑO =====
            file_size_bytes = os.path.getsize(audio_path)
            valid, error = validator.validate_audio_size(file_size_bytes, MAX_AUDIO_SIZE_MB)
            if not valid:
                raise ValueError(f"Tamaño inválido: {error}")
            
            # ===== RATE LIMITING =====
            if not gemini_limiter.is_allowed("transcription"):
                wait_time = gemini_limiter.get_wait_time("transcription")
                error_msg = f"⚠️  Límite de API excedido. Intenta en {wait_time:.1f}s"
                logger.warning(error_msg)
                raise RuntimeError(error_msg)
            
            # ===== TRANSCRIPCIÓN =====
            ext = audio_path.lower().split('.')[-1]
            mime_type = MIME_TYPES.get(ext, 'audio/mpeg')
            
            logger.info(f"Transcribiendo: {audio_path} ({mime_type})")
            audio_file = genai.upload_file(audio_path, mime_type=mime_type)
            
            prompt = "Transcribe el audio en texto. Solo devuelve el texto sin explicaciones."
            response = self.model.generate_content([prompt, audio_file])
            
            # Validar resultado
            if not response.text or len(response.text.strip()) == 0:
                raise ValueError("La transcripción resultó vacía")
            
            logger.info(f"✓ Transcripción: {len(response.text)} caracteres")
            
            class Result:
                def __init__(self, text):
                    self.text = text
            
            return Result(response.text)
        
        except FileNotFoundError as e:
            logger.error(f"Archivo no encontrado: {audio_path}")
            raise
        
        except ValueError as e:
            logger.error(f"transcript_audio: Validación - {str(e)}")
            raise
        
        except RuntimeError as e:
            # Rate limit exceed
            logger.error(f"transcript_audio: {str(e)}")
            raise
        
        except Exception as e:
            logger.error(f"transcript_audio: {type(e).__name__} - {str(e)}")
            raise

