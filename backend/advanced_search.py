"""advanced_search.py - Búsqueda full-text mejorada con filtros"""

from typing import List, Dict, Optional
from datetime import datetime
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger
from input_validator import validator

logger = get_logger(__name__)

class AdvancedSearch:
    """Motor de búsqueda avanzada para transcripciones y oportunidades"""
    
    @staticmethod
    def search_transcriptions(
        recordings: List[str],
        query: str = "",
        filters: Optional[Dict] = None
    ) -> List[str]:
        """Busca transcripciones con filtros avanzados
        
        Args:
            recordings: Lista de nombres de archivos
            query: Término de búsqueda
            filters: Dict con filtros:
                {
                    'date_from': '2025-02-01',
                    'date_to': '2025-02-11',
                    'status': 'transcribed|pending',
                    'duration_min': 60,  # segundos
                    'duration_max': 3600
                }
        
        Returns:
            Lista filtrada de grabaciones
        """
        try:
            results = recordings.copy()
            
            # ===== FILTRO 1: BÚSQUEDA POR TÉRMINO =====
            if query and query.strip():
                valid, error = validator.validate_search_query(query)
                if not valid:
                    logger.warning(f"Search query inválido: {error}")
                    return []
                
                search_term = query.lower()
                results = [r for r in results if search_term in r.lower()]
                logger.debug(f"Búsqueda '{query}': {len(results)} resultados")
            
            # ===== FILTRO 2: POR FECHA =====
            if filters and ('date_from' in filters or 'date_to' in filters):
                results = AdvancedSearch._filter_by_date(results, filters)
            
            # ===== FILTRO 3: POR NOMBRE PATRÓN =====
            if filters and 'pattern' in filters:
                pattern = filters['pattern']
                try:
                    regex = re.compile(pattern, re.IGNORECASE)
                    results = [r for r in results if regex.search(r)]
                    logger.debug(f"Filtro patrón '{pattern}': {len(results)} resultados")
                except re.error:
                    logger.warning(f"Patrón regex inválido: {pattern}")
            
            logger.info(f"✓ Búsqueda completada: {len(results)} resultados")
            return results
        
        except Exception as e:
            logger.error(f"search_transcriptions: {type(e).__name__} - {str(e)}")
            return recordings
    
    @staticmethod
    def _filter_by_date(recordings: List[str], filters: Dict) -> List[str]:
        """Filtra grabaciones por fecha basado en el nombre del archivo
        
        Asume formato: recording_YYYYMMDD_HHMMSS.ext o recording_2025-02-11.wav
        
        Args:
            recordings: Lista de nombres de archivo
            filters: Dict con 'date_from' y/o 'date_to' (formato YYYY-MM-DD)
        
        Returns:
            Lista filtrada
        """
        try:
            date_from = None
            date_to = None
            
            if 'date_from' in filters and filters['date_from']:
                date_from = datetime.strptime(filters['date_from'], '%Y-%m-%d')
            
            if 'date_to' in filters and filters['date_to']:
                date_to = datetime.strptime(filters['date_to'], '%Y-%m-%d')
            
            filtered = []
            
            for filename in recordings:
                # Extraer fecha del nombre (ej: recording_20250211_120000.wav)
                match = re.search(r'(\d{4})(\d{2})(\d{2})', filename)
                
                if not match:
                    # Si no encuentra patrón, incluir el archivo
                    filtered.append(filename)
                    continue
                
                year, month, day = match.groups()
                file_date = datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d')
                
                # Aplicar filtros de fecha
                if date_from and file_date < date_from:
                    continue
                if date_to and file_date > date_to:
                    continue
                
                filtered.append(filename)
            
            logger.debug(f"Filtro fecha: {len(filtered)} resultados")
            return filtered
        
        except Exception as e:
            logger.error(f"_filter_by_date: {str(e)}")
            return recordings
    
    @staticmethod
    def search_opportunities(
        opportunities: List[Dict],
        query: str = "",
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """Busca oportunidades con filtros avanzados
        
        Args:
            opportunities: Lista de oportunidades (dicts)
            query: Término de búsqueda
            filters: Dict con filtros:
                {
                    'status': 'new|in_progress|closed|won',
                    'priority': 'Low|Medium|High',
                    'keywords': ['keyword1', 'keyword2']
                }
        
        Returns:
            Lista filtrada de oportunidades
        """
        try:
            results = opportunities.copy()
            
            # ===== FILTRO 1: BÚSQUEDA POR TÉRMINO =====
            if query and query.strip():
                valid, error = validator.validate_search_query(query)
                if not valid:
                    logger.warning(f"Search query inválido: {error}")
                    return []
                
                search_term = query.lower()
                results = [
                    o for o in results 
                    if (search_term in o.get('title', '').lower() or 
                        search_term in o.get('description', '').lower() or
                        search_term in o.get('keyword', '').lower())
                ]
                logger.debug(f"Búsqueda '{query}': {len(results)} oportunidades")
            
            # ===== FILTRO 2: POR STATUS =====
            if filters and 'status' in filters:
                status = filters['status']
                results = [o for o in results if o.get('status') == status]
                logger.debug(f"Filtro status '{status}': {len(results)} oportunidades")
            
            # ===== FILTRO 3: POR PRIORIDAD =====
            if filters and 'priority' in filters:
                priority = filters['priority']
                results = [o for o in results if o.get('priority') == priority]
                logger.debug(f"Filtro prioridad '{priority}': {len(results)} oportunidades")
            
            # ===== FILTRO 4: POR KEYWORDS =====
            if filters and 'keywords' in filters:
                keywords = filters['keywords']
                results = [
                    o for o in results 
                    if o.get('keyword') in keywords
                ]
                logger.debug(f"Filtro keywords: {len(results)} oportunidades")
            
            logger.info(f"✓ Búsqueda de oportunidades completada: {len(results)} resultados")
            return results
        
        except Exception as e:
            logger.error(f"search_opportunities: {type(e).__name__} - {str(e)}")
            return opportunities

# Instancia global
searcher = AdvancedSearch()
