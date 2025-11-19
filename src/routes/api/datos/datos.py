from fastapi import APIRouter
from src.services.investigador_service import investigador_service
from src.utils.logger import logger
from src.utils.exceptions import APIException

router = APIRouter(prefix='/api/datos', tags=['Datos'])

@router.get('')
async def get_datos():
    try:
        return investigador_service.obtener_todos()
    except Exception as e:
        logger.error(f"Error inesperado en get_datos: {e}")
        raise APIException("Error interno del servidor", 500)

