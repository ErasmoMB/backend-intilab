from pathlib import Path
from fastapi import HTTPException
import json
from typing import Any
from src.utils.logger import logger

CACHE_DIR = Path("cache")

def load_json_file(filename: str):
    try:
        file_path = CACHE_DIR / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"Archivo {filename} no encontrado en cache")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error al decodificar JSON {filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo JSON {filename}")
    except Exception as e:
        logger.error(f"Error al cargar {filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al cargar {filename}")

def save_json_file(filename: str, data: Any) -> None:
    try:
        CACHE_DIR.mkdir(exist_ok=True)
        file_path = CACHE_DIR / filename
        if file_path.exists():
            file_path.unlink()
            logger.info(f"Archivo JSON existente eliminado: {filename}")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Archivo JSON guardado: {filename}")
    except Exception as e:
        logger.error(f"Error al guardar archivo JSON {filename}: {e}")

