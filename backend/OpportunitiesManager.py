"""OpportunitiesManager.py - Extrae oportunidades (300 → 140 líneas)"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import streamlit as st
import sys
import google.generativeai as genai
import re

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger
from database import init_supabase
from helpers import safe_json_dump
from config import GEMINI_API_KEY

logger = get_logger(__name__)
BASE_DIR = Path(__file__).parent.parent / "data" / "opportunities"
KEYWORDS_DICT_PATH = Path(__file__).parent.parent / "keywords_dict.json"

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)

class OpportunitiesManager:
    def __init__(self):
        BASE_DIR.mkdir(parents=True, exist_ok=True)
        self.db = init_supabase()
    
    def get_recording_id(self, filename: str) -> Optional[str]:
        """Obtiene ID del recording - intenta múltiples variaciones del nombre"""
        try:
            if not self.db:
                logger.warning(f"DB unavailable: {filename}")
                return None
            
            # Intentar búsqueda directa
            result = self.db.table("recordings").select("id").eq("filename", filename).execute()
            if result.data:
                recording_id = result.data[0]["id"]
                logger.info(f"✅ Recording encontrado (búsqueda exacta): {recording_id}")
                return recording_id
            
            # Si no encuentra, intentar variaciones
            logger.warning(f"No encontrado exacto: {filename}, probando variaciones...")
            
            # Variación 1: Buscar por nombre sin extensión
            filename_no_ext = filename.rsplit('.', 1)[0] if '.' in filename else filename
            result = self.db.table("recordings").select("id").eq("filename", filename_no_ext).execute()
            if result.data:
                recording_id = result.data[0]["id"]
                logger.info(f"✅ Recording encontrado (sin extensión): {recording_id}")
                return recording_id
            
            # Variación 2: Obtener todos los recordings y buscar por coincidencia parcial
            try:
                all_recordings = self.db.table("recordings").select("id, filename").order("created_at", desc=True).limit(20).execute()
                if all_recordings.data:
                    main_part = filename.split(" - ")[0].strip() if " - " in filename else filename_no_ext[:20]
                    for rec in all_recordings.data:
                        if main_part.lower() in rec["filename"].lower():
                            recording_id = rec["id"]
                            logger.info(f"✅ Recording encontrado (coincidencia parcial): {recording_id} ({rec['filename']})")
                            return recording_id
            except Exception as search_error:
                logger.debug(f"Búsqueda por coincidencia falló: {search_error}")
            
            logger.error(f"❌ Recording no encontrado con ninguna variación: {filename}")
            return None
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
            logger.info(f"📂 Cargando oportunidades para: {audio_filename}")
            
            if not self.db:
                logger.warning(f"BD unavailable, loading local: {audio_filename}")
                return self._load_local(audio_filename)
            
            # Obtener recording_id
            recording_id = self.get_recording_id(audio_filename)
            if not recording_id:
                logger.warning(f"⚠️  Recording ID no encontrado para '{audio_filename}', fallback local")
                return self._load_local(audio_filename)
            
            logger.info(f"🔍 Buscando opportunities con recording_id: {recording_id}")
            result = self.db.table("opportunities").select("*").eq("recording_id", recording_id).execute()
            
            if not result.data:
                logger.warning(f"❌ No opportunities encontradas para recording_id: {recording_id}")
                return []
            
            logger.info(f"✅ Encontradas {len(result.data)} opportunities")
            
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
            
            logger.info(f"✓ Cargadas {len(opportunities)} opportunities")
            return opportunities
        
        except Exception as e:
            logger.error(f"load_opportunities: {type(e).__name__} - {str(e)}")
            import traceback
            logger.debug(traceback.format_exc())
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
    
    def load_keywords_dict(self) -> Dict:
        """Carga el diccionario de keywords desde JSON"""
        try:
            if not KEYWORDS_DICT_PATH.exists():
                logger.warning(f"Keywords dict not found at {KEYWORDS_DICT_PATH}")
                return {}
            
            with open(KEYWORDS_DICT_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading keywords dict: {type(e).__name__} - {str(e)}")
            return {}
    
    def extract_speakers_from_transcription(self, transcription: str) -> Dict[str, List[str]]:
        """Extrae speakers y sus fragmentos de la transcripción con formato 'Nombre: "..."'"""
        speakers = {}
        try:
            # Patrón para detectar "Nombre: "texto""
            pattern = r'^([^:]+):\s*["\']?(.+?)["\']?\s*$'
            
            for line in transcription.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                match = re.match(pattern, line)
                if match:
                    speaker = match.group(1).strip()
                    text = match.group(2).strip()
                    
                    if speaker not in speakers:
                        speakers[speaker] = []
                    speakers[speaker].append(text)
            
            return speakers if speakers else {"Unknown": [transcription]}
        except Exception as e:
            logger.error(f"Error extracting speakers: {type(e).__name__} - {str(e)}")
            return {"Unknown": [transcription]}
    
    def analyze_opportunities_with_ai(
        self, 
        transcription: str, 
        audio_filename: str,
        recording_id: str = None
    ) -> Tuple[int, List[Dict]]:
        """
        Análisis inteligente de oportunidades usando Gemini.
        Detección de intenciones y conceptos, no solo palabras clave exactas.
        
        Args:
            transcription: Texto completo de la transcripción
            audio_filename: Nombre del archivo de audio para asociar la oportunidad
            recording_id: (Opcional) ID del recording en Supabase. Si se proporciona, se usa directamente.
                         Si no, se intenta obtener buscando por audio_filename.
        
        Returns:
            Tuple con (número de oportunidades detectadas, lista de oportunidades)
        """
        try:
            # Cargar diccionario de keywords
            keywords_dict = self.load_keywords_dict()
            if not keywords_dict:
                logger.warning("Keywords dict is empty, skipping AI analysis")
                return 0, []
            
            # Extraer speakers de la transcripción
            speakers = self.extract_speakers_from_transcription(transcription)
            logger.info(f"Speakers detectados: {list(speakers.keys())}")
            
            # Preparar lista de temas
            temas = keywords_dict.get("temas_de_interes", {})
            config = keywords_dict.get("configuracion", {})
            
            if not temas:
                logger.warning("No topics found in keywords dict")
                return 0, []
            
            speakers_list = ", ".join(speakers.keys())
            
            # Limitar transcripción si es necesario
            transcription_limited = transcription[:12000] if len(transcription) > 12000 else transcription
            
            # PROMPT EXTREMADAMENTE DIRECTO
            prompt = f"""CRÍTICO: Analiza esta conversación/reunión palabra por palabra. Detecta TODAS las oportunidades que encuentres.

MAPEO SIMPLE:
• Presupuesto / dinero / gasto / inversión / coste → "Presupuesto" (HIGH)
• Contactar / llamar / tarea / acción / hacer / pendiente / debe / responsabilidad → "Acción requerida" (HIGH)
• Regulación / ley / cumplimiento / compliance / auditoría / riesgo legal → "Cumplimiento Legal" (HIGH)
• Formación / capacitación / entrenamiento / curso / educación → "Formación" (MEDIUM)
• Contratar / empleado / personal / equipo / rol / recurso humano → "Recursos Humanos" (MEDIUM)
• Cliente / venta / deal / contrato / negocio / oportunidad / acuerdo → "Cierre de venta" (HIGH)
• Decisión / cambio / estrategia / importante / aprobado → "Decisión importante" (HIGH)
• Herramienta / infraestructura / sistema / plataforma / equipo tecnológico → "Infraestructura" (MEDIUM)

TRANSCRIPCIÓN:
{transcription_limited}

SPEAKERS: {speakers_list}

RESPONDE SOLO CON JSON (sin markdown, sin explicaciones):

{{"analisis_completo": true, "oportunidades": [{{"tema": "TemaExacto", "prioridad": "high/medium/low", "mencionado_por": "Nombre", "contexto": "frase", "confianza": 0.85}}]}}

Si no hay oportunidades: {{"analisis_completo": true, "oportunidades": []}}"""
            
            # Llamar a Gemini
            logger.info(f"Iniciando analisis con Gemini para: {audio_filename}")
            logger.info(f"Modelo: {config.get('modelo_gemini', 'gemini-2.0-flash')}")
            logger.info(f"Transcripción: {len(transcription_limited)} caracteres, Speakers: {speakers_list}")
            
            model = genai.GenerativeModel(config.get("modelo_gemini", "gemini-2.0-flash"))
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            logger.info(f"Respuesta Gemini recibida: {len(response_text)} caracteres")
            logger.info(f"RESPUESTA COMPLETA:\n{response_text}")
            
            # Limpiar respuesta
            # Remover markdown code blocks
            if "```json" in response_text:
                logger.info("Limpiando: encontrado ```json")
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                logger.info("Limpiando: encontrado ```")
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Remover caracteres de control
            response_text = response_text.strip()
            logger.info(f"Texto limpio: {response_text[:200]}")
            
            # Parsear JSON
            try:
                response_json = json.loads(response_text)
                logger.info(f"JSON parseado exitosamente: {response_json}")
            except json.JSONDecodeError as e:
                logger.error(f"ERROR al parsear JSON: {str(e)[:100]}")
                logger.error(f"Response text: {response_text[:300]}")
                # Intentar limpiar y reparsear
                try:
                    # Buscar el primer { y último }
                    start = response_text.find("{")
                    end = response_text.rfind("}") + 1
                    if start >= 0 and end > start:
                        cleaned = response_text[start:end]
                        logger.info(f"Intentando limpiar JSON desde {start} a {end}")
                        response_json = json.loads(cleaned)
                        logger.info("JSON recuperado tras limpieza")
                    else:
                        logger.error("No JSON encontrado en respuesta")
                        return 0, []
                except Exception as clean_err:
                    logger.error(f"Error en cleanup: {str(clean_err)[:100]}")
                    return 0, []
            
            oportunidades_data = response_json.get("oportunidades", [])
            logger.info(f"IA detectó {len(oportunidades_data)} oportunidades: {oportunidades_data}")
            
            if not oportunidades_data:
                logger.info(f"Análisis completado: 0 oportunidades detectadas")
                return 0, []
            
            # Obtener recording_id: usar el pasado como parámetro o buscar por nombre
            recording_id = recording_id or self.get_recording_id(audio_filename)
            
            logger.info(f"Recording ID obtenido: {recording_id}")
            
            # Si no hay recording_id, intentar crear uno
            if not recording_id:
                logger.warning(f"⚠️  Recording ID no encontrado para {audio_filename}, intentando crear...")
                try:
                    if not self.db:
                        logger.error(f"❌ DB no disponible para crear recording")
                    else:
                        # Crear un registro en la tabla recordings
                        new_recording = {
                            "filename": audio_filename,
                            "created_at": datetime.now().isoformat(),
                            "file_size_mb": 0.0,
                            "duration_seconds": 0,
                            "filepath": "",
                            "transcription": None
                        }
                        logger.info(f"Creando recording con filename: {audio_filename}")
                        result = self.db.table("recordings").insert(new_recording).execute()
                        if result.data and len(result.data) > 0:
                            recording_id = result.data[0].get("id")
                            logger.info(f"✅ Recording creado exitosamente: {recording_id}")
                        else:
                            logger.error(f"❌ Respuesta vacía al crear recording")
                except Exception as create_error:
                    logger.error(f"❌ Error al crear recording: {type(create_error).__name__} - {str(create_error)[:150]}")
            
            # Si aún no hay recording_id, no se puede guardar
            if not recording_id:
                logger.error(f"❌ No recording_id disponible después de intentos, no se guardarán las {len(oportunidades_data)} oportunidades")
                return len(oportunidades_data), []
            
            logger.info(f"✅ Usando recording_id para guardar oportunidades: {recording_id}")
            logger.info(f"📊 Total de oportunidades a guardar: {len(oportunidades_data)}")
            
            # Guardar cada oportunidad
            saved_opportunities = []
            for idx, opp in enumerate(oportunidades_data, 1):
                try:
                    tema = str(opp.get("tema", "")).strip()
                    mencionado_por = str(opp.get("mencionado_por", "Unknown")).strip()
                    contexto = str(opp.get("contexto", "")).strip()
                    confianza = float(opp.get("confianza", 0.8))
                    prioridad_str = str(opp.get("prioridad", "medium")).lower().strip()
                    
                    logger.debug(f"Opp {idx}: tema='{tema}', by='{mencionado_por}', conf={confianza:.2f}")
                    
                    # Validar tema
                    if tema not in temas:
                        logger.warning(f"❌ Opp {idx}: Tema '{tema}' NO está en diccionario. Temas válidos: {list(temas.keys())}")
                        continue
                    
                    # Validar confianza
                    min_confianza = float(config.get("minimo_confianza", 0.5))
                    if confianza < min_confianza:
                        logger.debug(f"⏭️  Opp {idx}: Confianza {confianza:.2f} < {min_confianza:.2f}, saltando")
                        continue
                    
                    if not contexto:
                        logger.warning(f"❌ Opp {idx}: Sin contexto, saltando")
                        continue
                    
                    # Mapear prioridades
                    priority_map = {"high": "High", "medium": "Medium", "low": "Low"}
                    priority = priority_map.get(prioridad_str, "Medium")
                    
                    # Construir nota
                    tema_data = temas.get(tema, {})
                    nota = f"🤖 TICKET GENERADO AUTOMÁTICAMENTE\n\n"
                    nota += f"📌 Tema: {tema}\n"
                    nota += f"📝 Descripción: {tema_data.get('descripcion', '')}\n"
                    nota += f"👤 Mencionado por: {mencionado_por}\n"
                    nota += f"💬 Contexto: {contexto}\n"
                    nota += f"🎯 Confianza: {confianza:.0%}"
                    
                    opportunity_data = {
                        "recording_id": recording_id,
                        "title": f"[IA] {tema} - {mencionado_por}",
                        "description": contexto,
                        "status": "new",
                        "priority": priority,
                        "notes": nota,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    logger.debug(f"Opp {idx}: Datos preparados para insertar")
                    
                    # Insertar en Supabase
                    if not self.db:
                        logger.error(f"❌ Opp {idx}: DB no disponible")
                        continue
                    
                    logger.debug(f"Opp {idx}: Iniciando insert en tabla opportunities...")
                    result = self.db.table("opportunities").insert(opportunity_data).execute()
                    
                    if result.data and len(result.data) > 0:
                        opp_id = result.data[0].get("id")
                        logger.info(f"✅ Opp {idx} guardada: {opp_id} | Tema: {tema} | Por: {mencionado_por}")
                        saved_opportunities.append(result.data[0])
                    else:
                        logger.error(f"❌ Opp {idx}: Respuesta vacía de Supabase")
                        logger.error(f"   Respuesta: {result}")
                    
                except Exception as inner_e:
                    logger.error(f"❌ Opp {idx}: Error {type(inner_e).__name__} - {str(inner_e)[:150]}")
                    import traceback
                    logger.debug(f"   Traceback: {traceback.format_exc()}")
            
            total = len(saved_opportunities)
            total_detectadas = len(oportunidades_data)
            logger.info(f"🎯 ANÁLISIS COMPLETADO: {total} guardadas / {total_detectadas} detectadas")
            
            # Retornar total detectadas (para mostrar feedback), y las guardadas (si existen)
            return total_detectadas, saved_opportunities
        
        except Exception as e:
            logger.error(f"analyze_opportunities_with_ai error: {type(e).__name__} - {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return 0, []

