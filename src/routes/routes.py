from fastapi import APIRouter
from src.services.investigador_service import investigador_service
from src.utils.logger import logger
from src.utils.exceptions import APIException

router = APIRouter()

@router.get('/datos')
async def datos_investigadores():
    try:
        return investigador_service.obtener_todos()
    except Exception as e:
        logger.error(f"Error en datos_investigadores: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/health')
async def health_check():
    return {"status": "healthy"}
