"""
Services - Lógica de negocio que usa los repositories
"""
from backend.services.audio_service import AudioService
from backend.services.transcription_service import TranscriptionService
from backend.services.opportunity_service import OpportunityService

__all__ = [
    "AudioService",
    "TranscriptionService", 
    "OpportunityService"
]
