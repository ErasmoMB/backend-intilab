import json
import os
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
from src.utils.logger import logger

CACHE_DIR = Path("cache")
CACHE_EXPIRY_HOURS = 24

def get_cache_path(cache_key: str) -> Path:
    CACHE_DIR.mkdir(exist_ok=True)
    safe_key = cache_key.replace("/", "_").replace(":", "_")
    return CACHE_DIR / f"{safe_key}.json"

def save_to_cache(cache_key: str, data: Any) -> None:
    try:
        cache_path = get_cache_path(cache_key)
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        logger.info(f"Datos guardados en caché: {cache_key}")
    except Exception as e:
        logger.error(f"Error al guardar en caché {cache_key}: {e}")

def load_from_cache(cache_key: str, max_age_hours: int = CACHE_EXPIRY_HOURS) -> Optional[Any]:
    try:
        cache_path = get_cache_path(cache_key)
        
        if not cache_path.exists():
            return None
        
        with open(cache_path, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        timestamp_str = cache_data.get("timestamp")
        if not timestamp_str:
            return None
        
        timestamp = datetime.fromisoformat(timestamp_str)
        age = datetime.now() - timestamp
        
        if age > timedelta(hours=max_age_hours):
            logger.info(f"Caché expirado para {cache_key}, edad: {age}")
            cache_path.unlink()
            return None
        
        logger.info(f"Datos cargados desde caché: {cache_key}, edad: {age}")
        return cache_data.get("data")
    except Exception as e:
        logger.error(f"Error al cargar desde caché {cache_key}: {e}")
        return None

def clear_cache(cache_key: Optional[str] = None) -> None:
    try:
        if cache_key:
            cache_path = get_cache_path(cache_key)
            if cache_path.exists():
                cache_path.unlink()
                logger.info(f"Caché eliminado: {cache_key}")
        else:
            if CACHE_DIR.exists():
                for file in CACHE_DIR.glob("*.json"):
                    file.unlink()
                logger.info("Todos los archivos de caché eliminados")
    except Exception as e:
        logger.error(f"Error al limpiar caché: {e}")

def get_cache_info(cache_key: str) -> Optional[Dict[str, Any]]:
    try:
        cache_path = get_cache_path(cache_key)
        if not cache_path.exists():
            return None
        
        with open(cache_path, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        timestamp_str = cache_data.get("timestamp")
        if timestamp_str:
            timestamp = datetime.fromisoformat(timestamp_str)
            age = datetime.now() - timestamp
            return {
                "exists": True,
                "timestamp": timestamp_str,
                "age_hours": age.total_seconds() / 3600,
                "size_bytes": cache_path.stat().st_size
            }
        return None
    except Exception as e:
        logger.error(f"Error al obtener info de caché {cache_key}: {e}")
        return None

