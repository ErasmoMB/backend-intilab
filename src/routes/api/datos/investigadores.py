from fastapi import APIRouter, HTTPException
from src.utils.file_loader import load_json_file
from src.utils.logger import logger

router = APIRouter(prefix='/api/datos/investigadores', tags=['Datos'])

@router.get('')
async def get_datos_investigadores():
    try:
        datos = load_json_file("datos_investigadores.json")
        return {"investigadores": datos, "source": "cache"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado en get_datos_investigadores: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

