from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from typing import List, Optional
from src.services.investigador_service import investigador_service
from src.middleware.auth import get_current_admin
from src.utils.exceptions import APIException, ValidationError, NotFoundError
from src.utils.logger import logger

router = APIRouter(prefix='/api/admin/investigadores', tags=['Admin - Investigadores'])

@router.get('')
async def obtener_investigadores(current_admin: dict = Depends(get_current_admin)):
    try:
        return investigador_service.obtener_todos()
    except Exception as e:
        logger.error(f"Error en obtener_investigadores: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/{id}')
async def obtener_investigador(id: str, current_admin: dict = Depends(get_current_admin)):
    try:
        return investigador_service.obtener_por_id(id)
    except (NotFoundError, ValidationError):
        raise
    except Exception as e:
        logger.error(f"Error en obtener_investigador: {e}")
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
        return await investigador_service.crear(
            autor_id=autor_id,
            nombre=nombre,
            grado_academico=grado_academico,
            imagen=imagen
        )
    except (ValidationError, APIException):
        raise
    except Exception as e:
        logger.error(f"Error en crear_investigador: {e}")
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
        return await investigador_service.actualizar(
            id=id,
            nombre=nombre,
            autor_id=autor_id,
            grado_academico=grado_academico,
            imagen=imagen if imagen and imagen.filename else None
        )
    except (NotFoundError, ValidationError, APIException):
        raise
    except Exception as e:
        logger.error(f"Error en actualizar_investigador: {e}")
        raise APIException("Error interno del servidor", 500)

@router.delete('/{id}')
async def eliminar_investigador(id: str, current_admin: dict = Depends(get_current_admin)):
    try:
        investigador_service.eliminar(id)
        return {'mensaje': 'Investigador eliminado correctamente'}
    except (NotFoundError, ValidationError):
        raise
    except Exception as e:
        logger.error(f"Error en eliminar_investigador: {e}")
        raise APIException("Error interno del servidor", 500)
