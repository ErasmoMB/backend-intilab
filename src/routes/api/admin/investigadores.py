from fastapi import APIRouter, Depends, File, UploadFile, Form
from typing import List, Optional
from src.services.investigador_service import investigador_service
from src.middleware.auth import get_current_admin
from src.utils.exceptions import APIException, ValidationError, NotFoundError
from src.utils.logger import logger

router = APIRouter(prefix='/api/admin/investigadores', tags=['Admin - Investigadores'])

@router.get('')
async def obtener_investigadores(current_admin: dict = Depends(get_current_admin)):
    try:
        investigadores = investigador_service.obtener_todos()
        return investigadores
    except Exception as e:
        logger.error(f"Error inesperado en obtener_investigadores: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/{id}')
async def obtener_investigador(id: str, current_admin: dict = Depends(get_current_admin)):
    try:
        investigador = investigador_service.obtener_por_id(id)
        return investigador
    except NotFoundError as e:
        raise e
    except ValidationError as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en obtener_investigador: {e}")
        raise APIException("Error interno del servidor", 500)

@router.post('', status_code=201)
async def crear_investigador(
    imagen: UploadFile = File(...),
    autor_id: str = Form(...),
    nombre: str = Form(...),
    grado_academico: List[str] = Form(...),
    current_admin: dict = Depends(get_current_admin)
):
    try:
        investigador = await investigador_service.crear(
            autor_id=autor_id,
            nombre=nombre,
            grado_academico=grado_academico,
            imagen=imagen
        )
        return investigador
    except ValidationError as e:
        raise e
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en crear_investigador: {e}")
        raise APIException("Error interno del servidor", 500)

@router.put('/{id}')
async def actualizar_investigador(
    id: str,
    nombre: Optional[str] = Form(None),
    autor_id: Optional[str] = Form(None),
    grado_academico: Optional[List[str]] = Form(None),
    imagen: Optional[UploadFile] = File(None),
    current_admin: dict = Depends(get_current_admin)
):
    try:
        investigador = await investigador_service.actualizar(
            id=id,
            nombre=nombre,
            autor_id=autor_id,
            grado_academico=grado_academico,
            imagen=imagen if imagen and imagen.filename else None
        )
        return investigador
    except NotFoundError as e:
        raise e
    except ValidationError as e:
        raise e
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en actualizar_investigador: {e}")
        raise APIException("Error interno del servidor", 500)

@router.delete('/{id}')
async def eliminar_investigador(id: str, current_admin: dict = Depends(get_current_admin)):
    try:
        investigador_service.eliminar(id)
        return {'mensaje': 'Investigador eliminado correctamente'}
    except NotFoundError as e:
        raise e
    except ValidationError as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en eliminar_investigador: {e}")
        raise APIException("Error interno del servidor", 500)
