"""
Repositories - Acceso a datos encapsulado
Separa la lógica de acceso a BD de la lógica de negocio
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from backend.supabase_client import get_db
from backend.validators import DataValidator

class BaseRepository:
    """Clase base para todos los repositories"""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.db = get_db()
    
    def _is_connected(self) -> bool:
        """Verifica si hay conexión a BD"""
        return self.db is not None


class RecordingRepository(BaseRepository):
    """Repository para la tabla 'recordings'"""
    
    def __init__(self):
        super().__init__("recordings")
    
    def create(self, filename: str, filepath: str, transcription: Optional[str] = None) -> Optional[int]:
        """
        Crea una grabación en la BD
        Returns: ID del recording creado o None si falla
        """
        if not self._is_connected():
            return None
        
        data = {
            "filename": filename,
            "filepath": filepath,
            "transcription": transcription,
            "created_at": datetime.now().isoformat()
        }
        
        # Validar datos
        is_valid, error_msg = DataValidator.validate_recording(data)
        if not is_valid:
            raise ValueError(error_msg)
        
        try:
            response = self.db.table(self.table_name).insert(data).execute()
            return response.data[0]["id"] if response.data else None
        except Exception as e:
            print(f"Error creando recording: {e}")
            return None
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Obtiene todas las grabaciones"""
        if not self._is_connected():
            return []
        
        try:
            response = self.db.table(self.table_name).select("*").order("created_at", desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error obteniendo grabaciones: {e}")
            return []
    
    def get_by_id(self, recording_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene una grabación por ID"""
        if not self._is_connected():
            return None
        
        try:
            response = self.db.table(self.table_name).select("*").eq("id", recording_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error obteniendo recording: {e}")
            return None
    
    def get_by_filename(self, filename: str) -> Optional[Dict[str, Any]]:
        """Obtiene una grabación por nombre de archivo"""
        if not self._is_connected():
            return None
        
        try:
            response = self.db.table(self.table_name).select("*").eq("filename", filename).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error obteniendo recording por filename: {e}")
            return None
    
    def update_transcription(self, recording_id: int, transcription: str) -> bool:
        """Actualiza la transcripción de una grabación"""
        if not self._is_connected():
            return False
        
        try:
            response = self.db.table(self.table_name).update({
                "transcription": transcription,
                "updated_at": datetime.now().isoformat()
            }).eq("id", recording_id).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error actualizando transcripción: {e}")
            return False
    
    def delete(self, recording_id: int) -> bool:
        """Elimina una grabación"""
        if not self._is_connected():
            return False
        
        try:
            # Primero eliminar las dependencias (cascada manual)
            TranscriptionRepository().delete_by_recording(recording_id)
            OpportunityRepository().delete_by_recording(recording_id)
            
            # Luego eliminar el recording
            response = self.db.table(self.table_name).delete().eq("id", recording_id).execute()
            return True
        except Exception as e:
            print(f"Error eliminando recording: {e}")
            return False


class TranscriptionRepository(BaseRepository):
    """Repository para la tabla 'transcriptions'"""
    
    def __init__(self):
        super().__init__("transcriptions")
    
    def create(self, recording_id: int, content: str, language: str = "es") -> Optional[int]:
        """Crea una transcripción"""
        if not self._is_connected():
            return None
        
        data = {
            "recording_id": recording_id,
            "content": content,
            "language": language,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Validar datos
        is_valid, error_msg = DataValidator.validate_transcription(data)
        if not is_valid:
            raise ValueError(error_msg)
        
        try:
            response = self.db.table(self.table_name).insert(data).execute()
            return response.data[0]["id"] if response.data else None
        except Exception as e:
            print(f"Error creando transcripción: {e}")
            return None
    
    def get_by_recording(self, recording_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene la transcripción más reciente de un recording"""
        if not self._is_connected():
            return None
        
        try:
            response = self.db.table(self.table_name)\
                .select("*")\
                .eq("recording_id", recording_id)\
                .order("created_at", desc=True)\
                .limit(1)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error obteniendo transcripción: {e}")
            return None
    
    def delete_by_recording(self, recording_id: int) -> bool:
        """Elimina todas las transcripciones de un recording"""
        if not self._is_connected():
            return False
        
        try:
            # Obtener todos los IDs primero
            response = self.db.table(self.table_name).select("id").eq("recording_id", recording_id).execute()
            
            if response.data:
                for transcription in response.data:
                    self.db.table(self.table_name).delete().eq("id", transcription["id"]).execute()
            
            return True
        except Exception as e:
            print(f"Error eliminando transcripciones: {e}")
            return False


class OpportunityRepository(BaseRepository):
    """Repository para la tabla 'opportunities'"""
    
    def __init__(self):
        super().__init__("opportunities")
    
    def create(self, recording_id: int, title: str, description: str = "") -> Optional[int]:
        """Crea una oportunidad"""
        if not self._is_connected():
            return None
        
        data = {
            "recording_id": recording_id,
            "title": title,
            "description": description,
            "created_at": datetime.now().isoformat()
        }
        
        # Validar datos
        is_valid, error_msg = DataValidator.validate_opportunity(data)
        if not is_valid:
            raise ValueError(error_msg)
        
        try:
            response = self.db.table(self.table_name).insert(data).execute()
            return response.data[0]["id"] if response.data else None
        except Exception as e:
            print(f"Error creando oportunidad: {e}")
            return None
    
    def get_by_recording(self, recording_id: int) -> List[Dict[str, Any]]:
        """Obtiene todas las oportunidades de un recording"""
        if not self._is_connected():
            return []
        
        try:
            response = self.db.table(self.table_name)\
                .select("*")\
                .eq("recording_id", recording_id)\
                .order("created_at", desc=True)\
                .execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error obteniendo oportunidades: {e}")
            return []
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Obtiene todas las oportunidades"""
        if not self._is_connected():
            return []
        
        try:
            response = self.db.table(self.table_name).select("*").order("created_at", desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error obteniendo oportunidades: {e}")
            return []
    
    def delete_by_recording(self, recording_id: int) -> bool:
        """Elimina todas las oportunidades de un recording"""
        if not self._is_connected():
            return False
        
        try:
            response = self.db.table(self.table_name).select("id").eq("recording_id", recording_id).execute()
            
            if response.data:
                for opportunity in response.data:
                    self.db.table(self.table_name).delete().eq("id", opportunity["id"]).execute()
            
            return True
        except Exception as e:
            print(f"Error eliminando oportunidades: {e}")
            return False
