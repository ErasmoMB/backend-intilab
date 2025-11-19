from fastapi import APIRouter, HTTPException
from src.utils.file_loader import load_json_file
from src.utils.logger import logger

router = APIRouter(prefix='/api/datos/authors', tags=['Datos'])

@router.get('')
async def get_autores():
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
    try:
        datos = load_json_file("autores_uch.json")
        if isinstance(datos, dict):
            if "total_autores_institucion" in datos and "total_autores_uch" not in datos:
                datos["total_autores_uch"] = datos.pop("total_autores_institucion")
        return {"autores_uch": datos, "source": "cache"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado en get_autores_uch: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

