from fastapi import APIRouter
from src.services.investigador_service import investigador_service
from src.utils.logger import logger

router = APIRouter()

@router.get('/datos')
async def datos_investigadores():
    try:
        investigadores = investigador_service.obtener_todos()
        return investigadores
    except Exception as e:
        logger.error(f"Error inesperado en datos_investigadores: {e}")
        return {"error": "Error interno del servidor"}

@router.get('/health')
async def health_check():
    return {"status": "healthy"}
