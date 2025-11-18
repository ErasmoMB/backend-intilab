from fastapi import APIRouter, Query
from src.services.scopus_service import scopus_service
from src.utils.exceptions import APIException
from src.utils.logger import logger

router = APIRouter(prefix='/api/scopus/documents', tags=['Scopus'])

AUTHOR_IDS = [
    "57210377414", "57225097710", "57203357446", "58562875900",
    "57205596738", "56741286500", "57215928001", "57215218631",
    "58127854500", "57223372908", "15750919900", "57209658640",
    "57205765369", "57364197600", "58886913200", "57930813500",
    "57204841219", "57211666738", "58077315000", "57207915215",
    "57016156500", "36659719000"
]

INSTITUCION_IDS = [
    "60110778", "60171637", "60171638", "60171644",
    "60171645", "60171646", "60171643", "60171647"
]

@router.get('')
async def fetch_documentos_from_scopus(au_id: str = Query(default=None)):
    try:
        if au_id:
            documentos = scopus_service.buscar_documentos(au_id, use_cache=False)
            return {'documentos': documentos, "source": "scopus"}
        
        documentos = {}
        for au_id_item in AUTHOR_IDS:
            documentos[au_id_item] = scopus_service.buscar_documentos(au_id_item, use_cache=False)
        return {'documentos': documentos, "source": "scopus"}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_documentos_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/ciics')
async def fetch_ciics_documents_from_scopus():
    try:
        documentos, status_code = scopus_service.buscar_documentos_afiliacion("60171638", use_cache=False)
        return {"documentos": documentos, "source": "scopus"}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_ciics_documents_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/e-health')
async def fetch_e_health_documents_from_scopus():
    try:
        documentos, status_code = scopus_service.buscar_documentos_afiliacion("60171643", use_cache=False)
        return {"documentos": documentos, "source": "scopus"}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_e_health_documents_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/inti-lab')
async def fetch_inti_lab_documents_from_scopus():
    try:
        documentos, status_code = scopus_service.buscar_documentos_afiliacion("60171637", use_cache=False)
        return {"documentos": documentos, "source": "scopus"}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_inti_lab_documents_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/uch')
async def fetch_uch_information_from_scopus():
    try:
        informacion = scopus_service.obtener_informacion_afiliaciones(INSTITUCION_IDS, use_cache=False)
        return {"informacion_afiliaciones": informacion, "source": "scopus"}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_uch_information_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)

