from fastapi import APIRouter, Depends, Body, UploadFile, File, Form
from typing import Optional, List, Dict, Any
from src.services.institucion_service import institucion_service
from src.services.s3_service import s3_service
from src.middleware.auth import get_current_admin
from src.utils.exceptions import APIException, ValidationError
from src.utils.logger import logger

router = APIRouter(prefix='/api/admin/institucion', tags=['Admin - Institución'])

@router.get('')
async def obtener_configuracion(current_admin: dict = Depends(get_current_admin)):
    try:
        config = institucion_service.obtener_configuracion()
        return config
    except Exception as e:
        logger.error(f"Error inesperado en obtener_configuracion: {e}")
        raise APIException("Error interno del servidor", 500)

@router.post('/upload-logo')
async def subir_logo(
    file: UploadFile = File(...),
    tipo: str = Form(...),
    current_admin: dict = Depends(get_current_admin)
):
    try:
        from src.utils.validators import validate_file_upload
        filename = validate_file_upload(file.filename)
        prefix = f"logos/{tipo}/"
        filename_with_prefix = f"{prefix}{filename}"
        url = await s3_service.upload_file(file, filename_with_prefix)
        return {"url": url}
    except Exception as e:
        logger.error(f"Error al subir logo: {e}")
        raise APIException("Error al subir el logo", 500)

@router.put('')
async def actualizar_configuracion(
    nombre: Optional[str] = Body(None),
    afiliacion_ids: Optional[List[str]] = Body(None),
    departamentos: Optional[Dict[str, Dict[str, str]]] = Body(None),
    logo_principal_url: Optional[str] = Body(None),
    fondo_slider_url: Optional[str] = Body(None),
    descripcion: Optional[str] = Body(None),
    configuracion_adicional: Optional[Dict[str, Any]] = Body(None),
    current_admin: dict = Depends(get_current_admin)
):
    try:
        if not any([nombre, afiliacion_ids, departamentos, logo_principal_url, fondo_slider_url, descripcion, configuracion_adicional]):
            raise ValidationError("Debe proporcionar al menos un campo para actualizar")
        
        if afiliacion_ids is not None and not isinstance(afiliacion_ids, list):
            raise ValidationError("afiliacion_ids debe ser una lista")
        
        if departamentos is not None and not isinstance(departamentos, dict):
            raise ValidationError("departamentos debe ser un diccionario")
        
        config = institucion_service.actualizar_configuracion(
            nombre=nombre,
            afiliacion_ids=afiliacion_ids,
            departamentos=departamentos,
            logo_principal_url=logo_principal_url,
            fondo_slider_url=fondo_slider_url,
            descripcion=descripcion,
            configuracion_adicional=configuracion_adicional
        )
        return config
    except ValidationError as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en actualizar_configuracion: {e}")
        raise APIException("Error interno del servidor", 500)

@router.post('/inicializar')
async def inicializar_configuracion(current_admin: dict = Depends(get_current_admin)):
    try:
        config = institucion_service.inicializar_con_defaults()
        return {
            "mensaje": "Configuración inicializada correctamente",
            "configuracion": config
        }
    except Exception as e:
        logger.error(f"Error inesperado en inicializar_configuracion: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/ids-afiliacion')
async def obtener_ids_afiliacion(current_admin: dict = Depends(get_current_admin)):
    try:
        ids = institucion_service.obtener_ids_afiliacion()
        return {"afiliacion_ids": ids}
    except Exception as e:
        logger.error(f"Error inesperado en obtener_ids_afiliacion: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/ids-investigadores')
async def obtener_ids_investigadores(current_admin: dict = Depends(get_current_admin)):
    try:
        ids = institucion_service.obtener_ids_investigadores()
        return {"investigador_ids": ids}
    except Exception as e:
        logger.error(f"Error inesperado en obtener_ids_investigadores: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/departamento/{clave}')
async def obtener_departamento(clave: str, current_admin: dict = Depends(get_current_admin)):
    try:
        departamento = institucion_service.obtener_departamento_por_clave(clave)
        if not departamento:
            raise APIException(f"Departamento '{clave}' no encontrado", 404)
        return {"departamento": departamento}
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en obtener_departamento: {e}")
        raise APIException("Error interno del servidor", 500)
