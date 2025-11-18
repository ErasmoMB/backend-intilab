from bson import ObjectId
from typing import List, Dict, Any, Optional
from fastapi import UploadFile
from src.config.database import db
from src.models.investigador import Investigador
from src.services.s3_service import s3_service
from src.utils.exceptions import NotFoundError, ValidationError
from src.utils.logger import logger

class InvestigadorService:
    def __init__(self):
        self.collection = db.get_collection()

    def _serialize_id(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        if '_id' in doc and isinstance(doc['_id'], ObjectId):
            doc['_id'] = str(doc['_id'])
        return doc

    def obtener_todos(self) -> List[Dict[str, Any]]:
        try:
            investigadores = list(self.collection.find())
            return [self._serialize_id(inv) for inv in investigadores]
        except Exception as e:
            logger.error(f"Error al obtener todos los investigadores: {e}")
            raise

    def obtener_por_id(self, id: str) -> Dict[str, Any]:
        try:
            object_id = ObjectId(id)
            investigador = self.collection.find_one({'_id': object_id})
            if not investigador:
                raise NotFoundError("Investigador no encontrado")
            return self._serialize_id(investigador)
        except ValueError:
            raise ValidationError("ID inválido")
        except Exception as e:
            logger.error(f"Error al obtener investigador por ID: {e}")
            raise

    async def crear(
        self,
        autor_id: str,
        nombre: str,
        grado_academico: List[str],
        imagen: Optional[UploadFile] = None
    ) -> Dict[str, Any]:
        try:
            ruta_imagen = ""
            
            if imagen and imagen.filename:
                from src.utils.validators import validate_file_upload
                filename = validate_file_upload(imagen.filename)
                ruta_imagen = await s3_service.upload_file(imagen, filename)
            
            nuevo_investigador = {
                'autor_id': autor_id,
                'nombre': nombre,
                'ruta_imagen': ruta_imagen,
                'grado_academico': grado_academico
            }
            
            result = self.collection.insert_one(nuevo_investigador)
            nuevo_investigador['_id'] = str(result.inserted_id)
            
            logger.info(f"Investigador creado con ID: {result.inserted_id}")
            return nuevo_investigador
        except Exception as e:
            logger.error(f"Error al crear investigador: {e}")
            raise

    async def actualizar(
        self,
        id: str,
        nombre: Optional[str] = None,
        autor_id: Optional[str] = None,
        grado_academico: Optional[List[str]] = None,
        imagen: Optional[UploadFile] = None
    ) -> Dict[str, Any]:
        try:
            object_id = ObjectId(id)
            update_data = {}
            
            if nombre is not None:
                update_data['nombre'] = nombre
            if autor_id is not None:
                update_data['autor_id'] = autor_id
            if grado_academico is not None:
                update_data['grado_academico'] = grado_academico
            
            if imagen:
                from src.utils.validators import validate_file_upload
                filename = validate_file_upload(imagen.filename)
                ruta_imagen = await s3_service.upload_file(imagen, filename)
                update_data['ruta_imagen'] = ruta_imagen
            
            if not update_data:
                raise ValidationError("No hay datos para actualizar")
            
            result = self.collection.update_one(
                {'_id': object_id},
                {'$set': update_data}
            )
            
            if result.matched_count == 0:
                raise NotFoundError("Investigador no encontrado")
            
            logger.info(f"Investigador actualizado con ID: {id}")
            return self.obtener_por_id(id)
        except ValueError:
            raise ValidationError("ID inválido")
        except Exception as e:
            logger.error(f"Error al actualizar investigador: {e}")
            raise

    def eliminar(self, id: str) -> None:
        try:
            object_id = ObjectId(id)
            result = self.collection.delete_one({'_id': object_id})
            
            if result.deleted_count == 0:
                raise NotFoundError("Investigador no encontrado")
            
            logger.info(f"Investigador eliminado con ID: {id}")
        except ValueError:
            raise ValidationError("ID inválido")
        except Exception as e:
            logger.error(f"Error al eliminar investigador: {e}")
            raise

investigador_service = InvestigadorService()

