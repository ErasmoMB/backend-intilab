from fastapi import APIRouter, HTTPException
from src.utils.file_loader import load_json_file
from src.utils.logger import logger

router = APIRouter(prefix='/api/datos/documents', tags=['Datos'])

@router.get('')
async def get_documentos():
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
    try:
        datos = load_json_file("informacion_uch.json")
        return {"informacion_uch": datos, "source": "cache"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado en get_informacion_uch: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

