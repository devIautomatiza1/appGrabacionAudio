"""sentiment_analyzer.py - Análisis de sentimiento con Gemini"""

import google.generativeai as genai
from pathlib import Path
import sys
from typing import Dict, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_API_KEY, CHAT_MODEL
from logger import get_logger
from rate_limiter import gemini_limiter
from input_validator import validator

logger = get_logger(__name__)
genai.configure(api_key=GEMINI_API_KEY)

class SentimentAnalyzer:
    """Analiza sentimiento de transcripciones usando Gemini"""
    
    def __init__(self):
        self.model = genai.GenerativeModel(CHAT_MODEL)
        logger.info("✓ Sentiment Analyzer initialized")
    
    def analyze(self, transcription: str) -> Optional[Dict]:
        """Analiza el sentimiento de una transcripción
        
        Args:
            transcription: Texto a analizar
            
        Returns:
            Dict con:
            {
                'sentiment': 'positivo|neutro|negativo',
                'score': 0.0-1.0,  # Confianza
                'emotions': ['emoción1', 'emoción2'],
                'summary': 'resumen del sentimiento'
            }
            
        Raises:
            RuntimeError: Si se excede rate limit
            ValueError: Si la entrada es inválida
        """
        try:
            # ===== VALIDACIÓN =====
            valid, error = validator.validate_transcription_text(transcription)
            if not valid:
                logger.error(f"Transcription inválida: {error}")
                raise ValueError(f"Transcripción inválida: {error}")
            
            # ===== RATE LIMITING =====
            if not gemini_limiter.is_allowed("sentiment"):
                wait_time = gemini_limiter.get_wait_time("sentiment")
                error_msg = f"⚠️  Límite de API excedido. Intenta en {wait_time:.1f}s"
                logger.warning(error_msg)
                raise RuntimeError(error_msg)
            
            # ===== ANÁLISIS DE SENTIMIENTO =====
            prompt = """Analiza el sentimiento del siguiente texto y responde en formato JSON:
{
    "sentiment": "positivo|neutro|negativo",
    "score": 0.0-1.0,
    "emotions": ["emoción1", "emoción2"],
    "summary": "resumen breve del sentimiento"
}

Texto:
{}

Responde SOLO con JSON válido, sin explicaciones adicionales.""".format(transcription[:1000])
            
            logger.info("Analizando sentimiento...")
            response = self.model.generate_content(prompt)
            
            # Parsear respuesta JSON
            import json
            try:
                sentiment_data = json.loads(response.text)
                logger.info(f"✓ Sentimiento: {sentiment_data['sentiment']}")
                return sentiment_data
            except json.JSONDecodeError:
                logger.warning("No se pudo parsear respuesta JSON, retornando formato simple")
                return {
                    "sentiment": "desconocido",
                    "score": 0.5,
                    "emotions": [],
                    "summary": "No se pudo analizar el sentimiento"
                }
        
        except ValueError as e:
            logger.error(f"analyze: Validación - {str(e)}")
            raise
        
        except RuntimeError as e:
            logger.error(f"analyze: {str(e)}")
            raise
        
        except Exception as e:
            logger.error(f"analyze: {type(e).__name__} - {str(e)}")
            raise

# Instancia global
sentiment_analyzer = SentimentAnalyzer()
