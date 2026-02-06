"""
Esquemas de datos - Definiciones de estructura para BD
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class RecordingSchema:
    """Schema para grabaciones de audio"""
    filename: str
    filepath: str
    transcription: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    id: Optional[int] = None
    
    def to_dict(self):
        """Convierte a diccionario para Supabase"""
        return {
            "filename": self.filename,
            "filepath": self.filepath,
            "transcription": self.transcription,
            "created_at": self.created_at or datetime.now().isoformat(),
        }

@dataclass
class TranscriptionSchema:
    """Schema para transcripciones"""
    recording_id: int
    content: str
    language: str = "es"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    id: Optional[int] = None
    
    def to_dict(self):
        """Convierte a diccionario para Supabase"""
        return {
            "recording_id": self.recording_id,
            "content": self.content,
            "language": self.language,
            "created_at": self.created_at or datetime.now().isoformat(),
            "updated_at": self.updated_at or datetime.now().isoformat(),
        }

@dataclass
class OpportunitySchema:
    """Schema para oportunidades"""
    recording_id: int
    title: str
    description: str = ""
    created_at: Optional[str] = None
    id: Optional[int] = None
    
    def to_dict(self):
        """Convierte a diccionario para Supabase"""
        return {
            "recording_id": self.recording_id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at or datetime.now().isoformat(),
        }
