from fastapi import APIRouter
from src.services.institucion_service import institucion_service
from src.utils.exceptions import APIException
from src.utils.logger import logger

router = APIRouter(prefix='/api/public/institucion', tags=['Public'])

@router.get('')
async def obtener_configuracion_publica():
    try:
        config = institucion_service.obtener_configuracion()
        return {
            "nombre": config.get("nombre", ""),
            "logo_principal_url": config.get("logo_principal_url", ""),
            "fondo_slider_url": config.get("fondo_slider_url", ""),
            "descripcion": config.get("descripcion", ""),
            "departamentos": config.get("departamentos", {})
        }
    except Exception as e:
        logger.error(f"Error inesperado en obtener_configuracion_publica: {e}")
        raise APIException("Error interno del servidor", 500)

