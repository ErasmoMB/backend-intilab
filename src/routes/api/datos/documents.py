from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from src.utils.logger import logger

router = APIRouter(prefix='/api/datos/documents', tags=['Datos'])

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
async def get_documentos():
    """Obtiene los documentos desde el archivo JSON en cache"""
    try:
        datos = load_json_file("documentos.json")
        return {"documentos": datos, "source": "cache"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado en get_documentos: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get('/uch')
async def get_informacion_uch():
    """Obtiene la información de afiliaciones UCH desde el archivo JSON en cache"""
    try:
        datos = load_json_file("informacion_uch.json")
        return {"informacion_uch": datos, "source": "cache"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado en get_informacion_uch: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

