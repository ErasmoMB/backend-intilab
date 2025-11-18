from fastapi import APIRouter, Depends, Query
from src.middleware.auth import get_current_admin
from src.utils.cache import clear_cache, get_cache_info
from src.utils.logger import logger

router = APIRouter(prefix='/api/admin/cache', tags=['Admin - Cache'])

@router.get('/info')
async def get_cache_info_endpoint(
    cache_key: str = Query(...),
    current_admin: dict = Depends(get_current_admin)
):
    try:
        info = get_cache_info(cache_key)
        if info:
            return info
        return {"exists": False}
    except Exception as e:
        logger.error(f"Error al obtener info de caché: {e}")
        return {"error": "Error interno del servidor"}

@router.delete('/clear')
async def clear_cache_endpoint(
    cache_key: str = Query(default=None),
    current_admin: dict = Depends(get_current_admin)
):
    try:
        clear_cache(cache_key)
        return {"mensaje": f"Caché {'eliminado' if cache_key else 'limpiado'} correctamente"}
    except Exception as e:
        logger.error(f"Error al limpiar caché: {e}")
        return {"error": "Error interno del servidor"}

