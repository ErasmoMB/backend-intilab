from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from src.utils.logger import logger

router = APIRouter(prefix='/api/datos/authors', tags=['Datos'])

CACHE_DIR = Path("cache")

def load_json_file(filename: str):
    """Carga un archivo JSON directamente del directorio cache"""
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

@router.get('')
async def get_autores():
    """Obtiene los autores desde el archivo JSON en cache"""
    try:
        datos = load_json_file("autores.json")
        return {"autores": datos, "source": "cache"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado en get_autores: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get('/uch')
async def get_autores_uch():
    """Obtiene los autores UCH desde el archivo JSON en cache"""
    try:
        datos = load_json_file("autores_uch.json")
        return {"autores_uch": datos, "source": "cache"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado en get_autores_uch: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

