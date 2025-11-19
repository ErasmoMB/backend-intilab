from bson import ObjectId
from typing import Optional, List, Dict, Any

DEFAULT_UCH_CONFIG = {
    "nombre": "Universidad de Ciencias y Humanidades",
    "afiliacion_ids": [
        "60110778", "60171637", "60171638", "60171644",
        "60171645", "60171646", "60171643", "60171647"
    ],
    "departamentos": {
        "ciics": {
            "af_id": "60171638",
            "nombre": "CIICS",
            "logo_url": ""
        },
        "e-health": {
            "af_id": "60171643",
            "nombre": "E-Health",
            "logo_url": ""
        },
        "inti-lab": {
            "af_id": "60171637",
            "nombre": "Inti-Lab",
            "logo_url": ""
        }
    },
    "logo_principal_url": "",
    "fondo_slider_url": "",
    "descripcion": "",
    "configuracion_adicional": {}
}

class Institucion:
    def __init__(
        self,
        nombre: str,
        afiliacion_ids: List[str],
        departamentos: Dict[str, Dict[str, str]],
        logo_principal_url: str = "",
        fondo_slider_url: str = "",
        descripcion: str = "",
        configuracion_adicional: Dict[str, Any] = None,
        _id: Optional[ObjectId] = None
    ):
        self._id = _id
        self.nombre = nombre
        self.afiliacion_ids = afiliacion_ids
        self.departamentos = departamentos
        self.logo_principal_url = logo_principal_url
        self.fondo_slider_url = fondo_slider_url
        self.descripcion = descripcion
        self.configuracion_adicional = configuracion_adicional or {}

    def to_dict(self) -> Dict[str, Any]:
        data = {
            'nombre': self.nombre,
            'afiliacion_ids': self.afiliacion_ids,
            'departamentos': self.departamentos,
            'logo_principal_url': self.logo_principal_url,
            'fondo_slider_url': self.fondo_slider_url,
            'descripcion': self.descripcion,
            'configuracion_adicional': self.configuracion_adicional
        }
        if self._id:
            data['_id'] = str(self._id)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Institucion':
        _id = data.get('_id')
        if isinstance(_id, str):
            _id = ObjectId(_id)
        elif isinstance(_id, ObjectId):
            pass
        else:
            _id = None

        return cls(
            nombre=data.get('nombre', DEFAULT_UCH_CONFIG['nombre']),
            afiliacion_ids=data.get('afiliacion_ids', DEFAULT_UCH_CONFIG['afiliacion_ids']),
            departamentos=data.get('departamentos', DEFAULT_UCH_CONFIG['departamentos']),
            logo_principal_url=data.get('logo_principal_url', ''),
            fondo_slider_url=data.get('fondo_slider_url', ''),
            descripcion=data.get('descripcion', ''),
            configuracion_adicional=data.get('configuracion_adicional', {}),
            _id=_id
        )

    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        return DEFAULT_UCH_CONFIG.copy()

