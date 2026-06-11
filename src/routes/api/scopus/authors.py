from fastapi import APIRouter, Query
from src.services.scopus_service import scopus_service
from src.services.investigador_service import investigador_service
from src.services.institucion_service import institucion_service
from src.utils.exceptions import APIException
from src.utils.logger import logger
from src.utils.file_loader import save_json_file

router = APIRouter(prefix='/api/scopus/authors', tags=['Scopus'])

def _fix_encoding(text: str) -> str:
    try:
        return text.encode("latin-1").decode("utf-8")
    except Exception:
        return text

def _build_names_map() -> dict:
    names_map = {}
    try:
        for inv in investigador_service.obtener_todos():
            autor_id = inv.get("autor_id")
            nombre = _fix_encoding(inv.get("nombre", ""))
            if not autor_id or not nombre:
                continue
            if ", " in nombre:
                parts = nombre.split(", ", 1)
                surname = parts[0].strip()
                given_name = parts[1].strip()
            else:
                parts = nombre.rsplit(" ", 1)
                surname = parts[1] if len(parts) == 2 else nombre
                given_name = parts[0] if len(parts) == 2 else ""
            names_map[autor_id] = {"surname": surname, "given-name": given_name}
    except Exception as e:
        logger.warning(f"No se pudo construir names_map: {e}")
    return names_map

@router.get('')
async def fetch_autores_from_scopus():
    try:
        investigador_ids = institucion_service.obtener_ids_investigadores()
        autores = scopus_service.buscar_autores(investigador_ids, use_cache=False, names_map=_build_names_map())
        save_json_file("autores.json", autores)
        return {"autores": autores, "source": "scopus"}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_autores_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/ids')
async def fetch_autores_por_ids_from_scopus(ids: list[str] = Query(default=None)):
    try:
        author_ids = ids if ids else institucion_service.obtener_ids_investigadores()
        autores = scopus_service.buscar_autores_por_ids(author_ids, use_cache=False, names_map=_build_names_map())
        save_json_file("autores.json", list(autores.values()) if isinstance(autores, dict) else autores)
        return {"autores": autores, "source": "scopus"}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_autores_por_ids_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/institucion')
async def fetch_autores_institucion():
    try:
        afiliacion_ids = institucion_service.obtener_ids_afiliacion()
        if not afiliacion_ids:
            return {"autores": [], "source": "scopus"}
        
        primary_af_id = afiliacion_ids[0]
        resultados = scopus_service.buscar_autores_uch(use_cache=False)
        resultados["source"] = "scopus"
        save_json_file("autores_uch.json", resultados)
        return resultados
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_autores_institucion: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/uch')
async def fetch_autores_uch_from_scopus():
    try:
        resultados = scopus_service.buscar_autores_uch(use_cache=False)
        resultados["source"] = "scopus"
        save_json_file("autores_uch.json", resultados)
        return resultados
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en fetch_autores_uch_from_scopus: {e}")
        raise APIException("Error interno del servidor", 500)
