from fastapi import APIRouter, Query
from src.services.scopus_service import scopus_service
from src.services.institucion_service import institucion_service
from src.utils.exceptions import APIException
from src.utils.logger import logger
from src.utils.file_loader import save_json_file, load_json_file

router = APIRouter(prefix='/api/scopus/documents', tags=['Scopus'])

@router.get('')
async def fetch_documentos_from_scopus(au_id: str = Query(default=None)):
    try:
        if au_id:
            documentos = scopus_service.buscar_documentos(au_id, use_cache=False)
            try:
                existing = load_json_file("documentos.json")
            except Exception:
                existing = {}
            existing[au_id] = documentos
            save_json_file("documentos.json", existing)
            return {'documentos': existing, "source": "scopus"}
        
        investigador_ids = institucion_service.obtener_ids_investigadores()
        documentos = {}
        for au_id_item in investigador_ids:
            documentos[au_id_item] = scopus_service.buscar_documentos(au_id_item, use_cache=False)
            save_json_file("documentos.json", documentos)
        return {'documentos': documentos, "source": "scopus"}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_documentos_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/institucion')
async def fetch_documentos_institucion():
    try:
        afiliacion_ids = institucion_service.obtener_ids_afiliacion()
        informacion = scopus_service.obtener_informacion_afiliaciones(afiliacion_ids, use_cache=False)
        save_json_file("informacion_uch.json", informacion)
        return {"informacion_uch": informacion, "source": "scopus"}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_documentos_institucion: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/departamento/{clave}')
async def fetch_documentos_departamento(clave: str):
    try:
        departamento = institucion_service.obtener_departamento_por_clave(clave)
        if not departamento:
            raise APIException(f"Departamento '{clave}' no encontrado", 404)
        
        af_id = departamento.get('af_id')
        if not af_id:
            raise APIException(f"Departamento '{clave}' no tiene ID de afiliación configurado", 400)
        
        documentos, status_code = scopus_service.buscar_documentos_afiliacion(af_id, use_cache=False)
        filename = f"documentos_{clave}.json"
        save_json_file(filename, documentos)
        return {"documentos": documentos, "source": "scopus", "departamento": clave}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_documentos_departamento: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/ciics')
async def fetch_ciics_documents_from_scopus():
    try:
        from src.models.institucion import DEFAULT_UCH_CONFIG
        departamento = institucion_service.obtener_departamento_por_clave('ciics')
        af_id = departamento.get('af_id') if departamento else DEFAULT_UCH_CONFIG['departamentos']['ciics']['af_id']
        documentos, status_code = scopus_service.buscar_documentos_afiliacion(af_id, use_cache=False)
        save_json_file("documentos_ciics.json", documentos)
        return {"documentos": documentos, "source": "scopus"}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_ciics_documents_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/e-health')
async def fetch_e_health_documents_from_scopus():
    try:
        from src.models.institucion import DEFAULT_UCH_CONFIG
        departamento = institucion_service.obtener_departamento_por_clave('e-health')
        af_id = departamento.get('af_id') if departamento else DEFAULT_UCH_CONFIG['departamentos']['e-health']['af_id']
        documentos, status_code = scopus_service.buscar_documentos_afiliacion(af_id, use_cache=False)
        save_json_file("documentos_e-health.json", documentos)
        return {"documentos": documentos, "source": "scopus"}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_e_health_documents_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/inti-lab')
async def fetch_inti_lab_documents_from_scopus():
    try:
        from src.models.institucion import DEFAULT_UCH_CONFIG
        departamento = institucion_service.obtener_departamento_por_clave('inti-lab')
        af_id = departamento.get('af_id') if departamento else DEFAULT_UCH_CONFIG['departamentos']['inti-lab']['af_id']
        documentos, status_code = scopus_service.buscar_documentos_afiliacion(af_id, use_cache=False)
        save_json_file("documentos_inti-lab.json", documentos)
        return {"documentos": documentos, "source": "scopus"}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_inti_lab_documents_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/uch')
async def fetch_uch_information_from_scopus():
    try:
        afiliacion_ids = institucion_service.obtener_ids_afiliacion()
        informacion = scopus_service.obtener_informacion_afiliaciones(afiliacion_ids, use_cache=False)
        save_json_file("informacion_uch.json", informacion)
        return {"informacion_uch": informacion, "source": "scopus"}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_uch_information_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)
