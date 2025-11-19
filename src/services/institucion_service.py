from bson import ObjectId
from typing import Dict, Any, Optional, List
from src.config.database import db
from src.models.institucion import Institucion, DEFAULT_UCH_CONFIG
from src.utils.exceptions import NotFoundError, ValidationError
from src.utils.logger import logger
from src.utils.serializers import serialize_id

class InstitucionService:
    COLLECTION_NAME = 'instituciones'

    def __init__(self):
        self.db = db.get_db()
        self.collection = None

    def _get_collection(self):
        if self.collection is None:
            if self.db is None:
                raise ConnectionError("No se pudo establecer conexión con MongoDB")
            self.collection = self.db[self.COLLECTION_NAME]
        return self.collection

    def _clean_empty_urls(self, config: Dict[str, Any]) -> Dict[str, Any]:
        cleaned = {}
        
        if '_id' in config:
            cleaned['_id'] = config['_id']
        
        if 'nombre' in config and config['nombre']:
            cleaned['nombre'] = config['nombre']
        
        if 'afiliacion_ids' in config and config['afiliacion_ids']:
            cleaned['afiliacion_ids'] = config['afiliacion_ids']
        
        if 'departamentos' in config and isinstance(config['departamentos'], dict):
            cleaned_dept = {}
            for clave, dept in config['departamentos'].items():
                if isinstance(dept, dict):
                    dept_cleaned = {}
                    if 'af_id' in dept and dept['af_id']:
                        dept_cleaned['af_id'] = dept['af_id']
                    if 'nombre' in dept and dept['nombre']:
                        dept_cleaned['nombre'] = dept['nombre']
                    if 'logo_url' in dept and dept['logo_url']:
                        dept_cleaned['logo_url'] = dept['logo_url']
                    if dept_cleaned:
                        cleaned_dept[clave] = dept_cleaned
                else:
                    cleaned_dept[clave] = dept
            if cleaned_dept:
                cleaned['departamentos'] = cleaned_dept
        
        if 'logo_principal_url' in config and config['logo_principal_url']:
            cleaned['logo_principal_url'] = config['logo_principal_url']
        
        if 'fondo_slider_url' in config and config['fondo_slider_url']:
            cleaned['fondo_slider_url'] = config['fondo_slider_url']
        
        if 'descripcion' in config and config['descripcion']:
            cleaned['descripcion'] = config['descripcion']
        
        if 'configuracion_adicional' in config and config['configuracion_adicional']:
            cleaned['configuracion_adicional'] = config['configuracion_adicional']
        
        return cleaned

    def _ensure_config_exists(self) -> Dict[str, Any]:
        collection = self._get_collection()
        existing = collection.find_one({})
        
        if existing is None:
            default_config = DEFAULT_UCH_CONFIG.copy()
            result = collection.insert_one(default_config)
            default_config['_id'] = str(result.inserted_id)
            logger.info("Configuración de institución inicializada con valores por defecto de UCH")
            return self._clean_empty_urls(serialize_id(default_config))
        
        config = serialize_id(existing)
        
        required_fields = {
            'nombre': DEFAULT_UCH_CONFIG.get('nombre', ''),
            'afiliacion_ids': DEFAULT_UCH_CONFIG.get('afiliacion_ids', []),
            'departamentos': DEFAULT_UCH_CONFIG.get('departamentos', {}),
        }
        
        update_needed = False
        update_data = {}
        
        for field, default_value in required_fields.items():
            if field not in config:
                config[field] = default_value
                update_data[field] = default_value
                update_needed = True
        
        if update_needed:
            collection.update_one({}, {'$set': update_data})
        
        return self._clean_empty_urls(config)

    def obtener_configuracion(self) -> Dict[str, Any]:
        try:
            return self._ensure_config_exists()
        except Exception as e:
            logger.error(f"Error al obtener configuración de institución: {e}")
            raise

    def obtener_ids_afiliacion(self) -> List[str]:
        try:
            config = self.obtener_configuracion()
            return config.get('afiliacion_ids', DEFAULT_UCH_CONFIG['afiliacion_ids'])
        except Exception as e:
            logger.error(f"Error al obtener IDs de afiliación: {e}")
            return DEFAULT_UCH_CONFIG['afiliacion_ids']

    def obtener_ids_investigadores(self) -> List[str]:
        try:
            from src.services.investigador_service import investigador_service
            investigadores = investigador_service.obtener_todos()
            autor_ids = [inv.get('autor_id') for inv in investigadores if inv.get('autor_id')]
            return list(filter(None, autor_ids))
        except Exception as e:
            logger.warning(f"Error al obtener IDs de investigadores desde DB, usando valores por defecto: {e}")
            return [
                "57210377414", "57225097710", "57203357446", "58562875900",
                "57205596738", "56741286500", "57215928001", "57215218631",
                "58127854500", "57223372908", "15750919900", "57209658640",
                "57205765369", "57364197600", "58886913200", "57930813500",
                "57204841219", "57211666738", "58077315000", "57207915215",
                "57016156500", "36659719000"
            ]

    def obtener_departamento_por_clave(self, clave: str) -> Optional[Dict[str, str]]:
        try:
            config = self.obtener_configuracion()
            departamentos = config.get('departamentos', {})
            return departamentos.get(clave)
        except Exception as e:
            logger.error(f"Error al obtener departamento {clave}: {e}")
            return None

    def actualizar_configuracion(
        self,
        nombre: Optional[str] = None,
        afiliacion_ids: Optional[List[str]] = None,
        departamentos: Optional[Dict[str, Dict[str, str]]] = None,
        logo_principal_url: Optional[str] = None,
        fondo_slider_url: Optional[str] = None,
        descripcion: Optional[str] = None,
        configuracion_adicional: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            collection = self._get_collection()
            self._ensure_config_exists()
            
            update_data = {}
            unset_data = {}
            
            if nombre is not None:
                update_data['nombre'] = nombre
            if afiliacion_ids is not None:
                update_data['afiliacion_ids'] = afiliacion_ids
            if departamentos is not None:
                update_data['departamentos'] = departamentos
            if logo_principal_url is not None:
                if logo_principal_url:
                    update_data['logo_principal_url'] = logo_principal_url
                else:
                    unset_data['logo_principal_url'] = ""
            if fondo_slider_url is not None:
                if fondo_slider_url:
                    update_data['fondo_slider_url'] = fondo_slider_url
                else:
                    unset_data['fondo_slider_url'] = ""
            if descripcion is not None:
                if descripcion:
                    update_data['descripcion'] = descripcion
                else:
                    unset_data['descripcion'] = ""
            if configuracion_adicional is not None:
                update_data['configuracion_adicional'] = configuracion_adicional

            if not update_data and not unset_data:
                raise ValidationError("No hay datos para actualizar")

            update_operation = {}
            if update_data:
                update_operation['$set'] = update_data
            if unset_data:
                update_operation['$unset'] = unset_data

            result = collection.update_one({}, update_operation)
            
            if result.matched_count == 0:
                self._ensure_config_exists()
                collection.update_one({}, update_operation)

            logger.info("Configuración de institución actualizada correctamente")
            return self.obtener_configuracion()
        except Exception as e:
            logger.error(f"Error al actualizar configuración de institución: {e}")
            raise

    def inicializar_con_defaults(self) -> Dict[str, Any]:
        try:
            collection = self._get_collection()
            existing = collection.find_one({})
            
            if existing is not None:
                logger.info("La configuración ya existe, no se inicializa")
                return self._clean_empty_urls(serialize_id(existing))
            
            default_config = DEFAULT_UCH_CONFIG.copy()
            result = collection.insert_one(default_config)
            default_config['_id'] = str(result.inserted_id)
            logger.info("Configuración de institución inicializada con valores por defecto")
            return self._clean_empty_urls(serialize_id(default_config))
        except Exception as e:
            logger.error(f"Error al inicializar configuración: {e}")
            raise

institucion_service = InstitucionService()

