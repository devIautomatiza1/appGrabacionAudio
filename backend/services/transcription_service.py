"""
Transcription Service - Lógica de negocio para transcripciones
"""
from typing import Optional, Dict, Any
from backend.database.repositories import RecordingRepository, TranscriptionRepository

class TranscriptionService:
    """Servicio de lógica de negocio para transcripciones"""
    
    def __init__(self):
        self.transcription_repo = TranscriptionRepository()
        self.recording_repo = RecordingRepository()
    
    def save_transcription(self, recording_id: int, content: str, language: str = "es") -> Optional[int]:
        """
        Guarda una transcripción en la BD
        Returns: ID de la transcripción creada
        """
        try:
            # Validar que el recording existe
            recording = self.recording_repo.get_by_id(recording_id)
            if not recording:
                raise ValueError(f"Recording con ID {recording_id} no existe")
            
            transcription_id = self.transcription_repo.create(recording_id, content, language)
            
            # Actualizar el campo transcription en la tabla recordings
            if transcription_id:
                self.recording_repo.update_transcription(recording_id, content[:500])  # Guardar preview
            
            return transcription_id
        except Exception as e:
            print(f"Error en TranscriptionService.save_transcription: {e}")
            return None
    
    def get_transcription(self, recording_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene la transcripción de un recording"""
        try:
            return self.transcription_repo.get_by_recording(recording_id)
        except Exception as e:
            print(f"Error en TranscriptionService.get_transcription: {e}")
            return None
    
    def update_transcription(self, recording_id: int, content: str) -> bool:
        """Actualiza una transcripción existente"""
        try:
            # Eliminar la anterior y crear una nueva
            self.transcription_repo.delete_by_recording(recording_id)
            self.save_transcription(recording_id, content)
            return True
        except Exception as e:
            print(f"Error en TranscriptionService.update_transcription: {e}")
            return False
