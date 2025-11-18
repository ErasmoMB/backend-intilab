from fastapi import APIRouter, Query
from src.services.scopus_service import scopus_service
from src.utils.exceptions import APIException
from src.utils.logger import logger

router = APIRouter(prefix='/api/scopus/authors', tags=['Scopus'])

AUTHOR_IDS = [
    "57210377414", "57225097710", "57203357446", "58562875900",
    "57205596738", "56741286500", "57215928001", "57215218631",
    "58127854500", "57223372908", "15750919900", "57209658640",
    "57205765369", "57364197600", "58886913200", "57930813500",
    "57204841219", "57211666738", "58077315000", "57207915215",
    "57016156500", "36659719000"
]

@router.get('')
async def fetch_autores_from_scopus():
    try:
        autores = scopus_service.buscar_autores(AUTHOR_IDS, use_cache=False)
        return {"autores": autores, "source": "scopus"}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_autores_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/ids')
async def fetch_autores_por_ids_from_scopus(ids: list[str] = Query(default=None)):
    try:
        author_ids = ids if ids else AUTHOR_IDS
        autores = scopus_service.buscar_autores_por_ids(author_ids, use_cache=False)
        return {"autores": autores, "source": "scopus"}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_autores_por_ids_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/uch')
async def fetch_autores_uch_from_scopus():
    try:
        resultados = scopus_service.buscar_autores_uch(use_cache=False)
        resultados["source"] = "scopus"
        return resultados
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_autores_uch_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)

