"""OpportunitiesManager.py - Extrae oportunidades (300 → 140 líneas)"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import streamlit as st
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger
from database import init_supabase
from helpers import safe_json_dump

logger = get_logger(__name__)
BASE_DIR = Path(__file__).parent.parent / "data" / "opportunities"

class OpportunitiesManager:
    def __init__(self):
        BASE_DIR.mkdir(parents=True, exist_ok=True)
        self.db = init_supabase()
    
    def get_recording_id(self, filename: str) -> Optional[str]:
        """Obtiene ID del recording"""
        try:
            if not self.db:
                logger.warning(f"DB unavailable: {filename}")
                return None
            result = self.db.table("recordings").select("id").eq("filename", filename).execute()
            recording_id = result.data[0]["id"] if result.data else None
            if recording_id:
                logger.debug(f"Recording ID: {recording_id}")
            else:
                logger.warning(f"Recording not found: {filename}")
            return recording_id
        except Exception as e:
            logger.error(f"get_recording_id: {type(e).__name__} - {str(e)}")
            return None
    
    def extract_opportunities(self, transcription: str, keywords_list: List[str]) -> List[Dict]:
        """Extrae oportunidades de keywords en transcripción"""
        if not keywords_list:
            return []
        
        opportunities, words = [], transcription.lower().split()
        for keyword in keywords_list:
            occurrence_count = 0
            for i, word in enumerate(words):
                if keyword.lower() not in word:
                    continue
                occurrence_count += 1
                context_window = 15
                start, end = max(0, i - context_window), min(len(words), i + context_window + 1)
                
                opportunity = {
                    "id": f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{keyword}_{occurrence_count}",
                    "keyword": keyword,
                    "context_before": " ".join(words[start:i]),
                    "context_after": " ".join(words[i+1:end]),
                    "full_context": f"{' '.join(words[start:i])} **{keyword}** {' '.join(words[i+1:end])}",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "new",
                    "notes": "",
                    "occurrence": occurrence_count,
                    "priority": "Medium",
                    "title": keyword
                }
                opportunities.append(opportunity)
        return opportunities
    
    def save_opportunity(self, opportunity: Dict, audio_filename: str) -> bool:
        """Guarda oportunidad en BD/local"""
        try:
            if not self.db:
                logger.warning(f"BD unavailable, saving locally: {audio_filename}")
                return self._save_local(opportunity, audio_filename)
            
            recording_id = self.get_recording_id(audio_filename)
            if not recording_id:
                logger.warning(f"Recording ID not found, fallback local")
                return self._save_local(opportunity, audio_filename)
            
            priority = opportunity.get("priority", "Medium").capitalize()
            data = {
                "recording_id": recording_id,
                "title": opportunity.get("keyword", "Opportunity"),
                "description": opportunity.get("full_context", ""),
                "status": opportunity.get("status", "new"),
                "priority": priority,
                "notes": opportunity.get("notes", ""),
                "created_at": datetime.now().isoformat()
            }
            
            result = self.db.table("opportunities").insert(data).execute()
            if result.data:
                supabase_id = result.data[0].get("id")
                opportunity["supabase_id"] = supabase_id
                opportunity["id"] = supabase_id
                logger.info(f"✓ Opportunity saved: {supabase_id}")
                return True
            
            logger.warning(f"Supabase empty response, fallback local")
            return self._save_local(opportunity, audio_filename)
        
        except Exception as e:
            logger.error(f"save_opportunity: {type(e).__name__} - {str(e)}")
            return self._save_local(opportunity, audio_filename)
    
    def _save_local(self, opportunity: Dict, audio_filename: str) -> bool:
        """Fallback: guarda JSON localmente"""
        filename = f"opp_{audio_filename.replace('.', '_')}_{opportunity['id']}.json"
        return safe_json_dump(opportunity, filename, BASE_DIR)
    
    def load_opportunities(self, audio_filename: str) -> List[Dict]:
        """Carga oportunidades desde BD/local"""
        try:
            if not self.db:
                logger.warning(f"BD unavailable, loading local: {audio_filename}")
                return self._load_local(audio_filename)
            
            recording_id = self.get_recording_id(audio_filename)
            if not recording_id:
                logger.warning(f"Recording ID not found, fallback local")
                return self._load_local(audio_filename)
            
            result = self.db.table("opportunities").select("*").eq("recording_id", recording_id).execute()
            if not result.data:
                logger.debug(f"No opportunities found for: {audio_filename}")
                return []
            
            opportunities = [{
                "id": r.get("id"),
                "supabase_id": r.get("id"),
                "keyword": r.get("title", ""),
                "full_context": r.get("description", ""),
                "status": r.get("status", "new"),
                "notes": r.get("notes", ""),
                "priority": r.get("priority", "Medium"),
                "created_at": r.get("created_at", ""),
                "occurrence": 1
            } for r in result.data]
            
            logger.info(f"✓ Loaded {len(opportunities)} opportunities")
            return opportunities
        
        except Exception as e:
            logger.error(f"load_opportunities: {type(e).__name__} - {str(e)}")
            return self._load_local(audio_filename)
    
    def _load_local(self, audio_filename: str) -> List[Dict]:
        """Carga oportunidades de archivos JSON locales"""
        opportunities = []
        try:
            pattern = f"opp_{audio_filename.replace('.', '_')}_*.json"
            for filepath in BASE_DIR.glob(pattern):
                with open(filepath, "r", encoding="utf-8") as f:
                    opportunities.append(json.load(f))
            return opportunities if opportunities else []
        except:
            return []
    
    def update_opportunity(self, opportunity_id: str, updates: Dict) -> bool:
        """Actualiza oportunidad"""
        try:
            if not self.db:
                logger.warning("BD unavailable for update")
                return False
            
            result = self.db.table("opportunities").update(updates).eq("id", opportunity_id).execute()
            if result.data:
                logger.info(f"✓ Opportunity updated: {opportunity_id}")
                return True
            
            logger.warning(f"Update returned empty")
            return False
        
        except Exception as e:
            logger.error(f"update_opportunity: {type(e).__name__} - {str(e)}")
            return False
    
    def delete_opportunity(self, opportunity_id: str) -> bool:
        """Elimina oportunidad"""
        try:
            if not self.db:
                logger.warning("BD unavailable for delete")
                return False
            
            result = self.db.table("opportunities").delete().eq("id", opportunity_id).execute()
            logger.info(f"✓ Opportunity deleted: {opportunity_id}")
            return True
        
        except Exception as e:
            logger.error(f"delete_opportunity: {type(e).__name__} - {str(e)}")
            return False
