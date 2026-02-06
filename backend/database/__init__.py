"""
Database layer - Acceso a BD encapsulado
"""
from backend.database.repositories import RecordingRepository, TranscriptionRepository, OpportunityRepository

__all__ = [
    "RecordingRepository",
    "TranscriptionRepository", 
    "OpportunityRepository"
]
