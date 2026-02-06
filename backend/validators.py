"""
Validadores de datos antes de ser almacenados en BD
"""
from typing import Dict, Any, Tuple

class DataValidator:
    """Validador centralizado para datos"""
    
    @staticmethod
    def validate_recording(data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Valida datos de una grabación
        Returns: (es_valido, mensaje_error)
        """
        if not isinstance(data, dict):
            return False, "Los datos deben ser un diccionario"
        
        if not data.get("filename") or not isinstance(data["filename"], str):
            return False, "El filename es requerido y debe ser string"
        
        if not data.get("filepath") or not isinstance(data["filepath"], str):
            return False, "El filepath es requerido y debe ser string"
        
        if len(data["filename"]) > 255:
            return False, "El filename no puede exceder 255 caracteres"
        
        return True, ""
    
    @staticmethod
    def validate_transcription(data: Dict[str, Any]) -> Tuple[bool, str]:
        """Valida datos de una transcripción"""
        if not isinstance(data, dict):
            return False, "Los datos deben ser un diccionario"
        
        if not data.get("content") or not isinstance(data["content"], str):
            return False, "El contenido es requerido y debe ser string"
        
        if not data.get("recording_id"):
            return False, "El recording_id es requerido"
        
        if len(data["content"]) > 50000:
            return False, "El contenido de transcripción es muy largo"
        
        return True, ""
    
    @staticmethod
    def validate_opportunity(data: Dict[str, Any]) -> Tuple[bool, str]:
        """Valida datos de una oportunidad"""
        if not isinstance(data, dict):
            return False, "Los datos deben ser un diccionario"
        
        if not data.get("title") or not isinstance(data["title"], str):
            return False, "El title es requerido y debe ser string"
        
        if not data.get("recording_id"):
            return False, "El recording_id es requerido"
        
        if len(data.get("description", "")) > 5000:
            return False, "La descripción es muy larga"
        
        return True, ""
