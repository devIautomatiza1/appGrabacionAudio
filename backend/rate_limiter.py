"""rate_limiter.py - Control de llamadas a APIs con rate limiting"""
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
from pathlib import Path
import sys
import json

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger
from config import RATE_LIMIT_CALLS, RATE_LIMIT_WINDOW, RATE_LIMIT_TOKENS

logger = get_logger(__name__)

class RateLimiter:
    """Limitador de velocidad para APIs externas"""
    
    def __init__(self, max_calls: int = RATE_LIMIT_CALLS, window_seconds: int = RATE_LIMIT_WINDOW):
        """
        Args:
            max_calls: Máximo número de llamadas permitidas
            window_seconds: Ventana de tiempo en segundos
        """
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls: Dict[str, list] = {}
    
    def is_allowed(self, user_id: str = "default") -> bool:
        """Verifica si se permite una nueva llamada
        
        Args:
            user_id: Identificador del usuario (default: "default")
            
        Returns:
            True si está permitido, False si se excedió el límite
        """
        now = datetime.now()
        
        # Limpiar llamadas antiguas
        if user_id not in self.calls:
            self.calls[user_id] = []
        
        # Remover llamadas fuera de la ventana de tiempo
        cutoff_time = now - timedelta(seconds=self.window_seconds)
        self.calls[user_id] = [
            call_time for call_time in self.calls[user_id]
            if call_time > cutoff_time
        ]
        
        # Verificar límite
        if len(self.calls[user_id]) >= self.max_calls:
            oldest_call = min(self.calls[user_id])
            wait_time = (oldest_call + timedelta(seconds=self.window_seconds) - now).total_seconds()
            logger.warning(
                f"⚠️  Rate limit excedido para {user_id}. "
                f"Espera {wait_time:.1f}s antes de reintentar"
            )
            return False
        
        # Registrar nueva llamada
        self.calls[user_id].append(now)
        logger.debug(f"✓ Llamada permitida ({len(self.calls[user_id])}/{self.max_calls})")
        return True
    
    def get_wait_time(self, user_id: str = "default") -> float:
        """Retorna tiempo de espera en segundos hasta la próxima llamada
        
        Args:
            user_id: Identificador del usuario
            
        Returns:
            Segundos que debe esperar, 0 si puede llamar inmediatamente
        """
        now = datetime.now()
        
        if user_id not in self.calls or not self.calls[user_id]:
            return 0
        
        # Limpiar llamadas antiguas
        cutoff_time = now - timedelta(seconds=self.window_seconds)
        self.calls[user_id] = [
            call_time for call_time in self.calls[user_id]
            if call_time > cutoff_time
        ]
        
        if len(self.calls[user_id]) < self.max_calls:
            return 0
        
        oldest_call = min(self.calls[user_id])
        wait_time = (oldest_call + timedelta(seconds=self.window_seconds) - now).total_seconds()
        return max(0, wait_time)
    
    def reset(self, user_id: str = "default") -> None:
        """Resetea el contador para un usuario
        
        Args:
            user_id: Identificador del usuario
        """
        if user_id in self.calls:
            self.calls[user_id] = []
            logger.info(f"✓ Rate limiter reseteado para {user_id}")

class TokenBucketLimiter:
    """Limitador de tokens con bucket (más flexible que rate limiter)
    
    Permite ráfagas mientras respeta límite general a largo plazo.
    """
    
    def __init__(self, capacity: int = RATE_LIMIT_TOKENS, refill_rate: float = 1.0):
        """
        Args:
            capacity: Máximo número de tokens en el bucket
            refill_rate: Tokens añadidos por segundo
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens: Dict[str, float] = {}
        self.last_refill: Dict[str, datetime] = {}
    
    def _refill(self, user_id: str) -> None:
        """Rellena los tokens basado en tiempo transcurrido"""
        now = datetime.now()
        
        if user_id not in self.last_refill:
            self.tokens[user_id] = self.capacity
            self.last_refill[user_id] = now
            return
        
        elapsed = (now - self.last_refill[user_id]).total_seconds()
        new_tokens = elapsed * self.refill_rate
        
        self.tokens[user_id] = min(
            self.capacity,
            self.tokens[user_id] + new_tokens
        )
        self.last_refill[user_id] = now
    
    def consume(self, tokens: float = 1.0, user_id: str = "default") -> bool:
        """Intenta consumir tokens
        
        Args:
            tokens: Número de tokens a consumir (default: 1)
            user_id: Identificador del usuario
            
        Returns:
            True si se consumieron los tokens, False si no hay suficientes
        """
        self._refill(user_id)
        
        if self.tokens[user_id] >= tokens:
            self.tokens[user_id] -= tokens
            logger.debug(f"✓ Tokens consumidos ({self.tokens[user_id]:.1f}/{self.capacity})")
            return True
        
        logger.warning(
            f"⚠️  Tokens insuficientes para {user_id}. "
            f"Disponibles: {self.tokens[user_id]:.1f}, Requeridos: {tokens}"
        )
        return False
    
    def get_available_tokens(self, user_id: str = "default") -> float:
        """Retorna número de tokens disponibles"""
        self._refill(user_id)
        return self.tokens[user_id]

# Instancia global
gemini_limiter = RateLimiter()
token_bucket = TokenBucketLimiter()
