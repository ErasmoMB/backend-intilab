from bson import ObjectId
from typing import Optional, List, Dict, Any

class Investigador:
    def __init__(
        self,
        autor_id: str,
        nombre: str,
        ruta_imagen: str,
        grado_academico: List[str],
        _id: Optional[ObjectId] = None
    ):
        self._id = _id
        self.autor_id = autor_id
        self.nombre = nombre
        self.ruta_imagen = ruta_imagen
        self.grado_academico = grado_academico

    def to_dict(self) -> Dict[str, Any]:
        data = {
            'autor_id': self.autor_id,
            'nombre': self.nombre,
            'ruta_imagen': self.ruta_imagen,
            'grado_academico': self.grado_academico
        }
        if self._id:
            data['_id'] = str(self._id)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Investigador':
        _id = data.get('_id')
        if isinstance(_id, str):
            _id = ObjectId(_id)
        elif isinstance(_id, ObjectId):
            pass
        else:
            _id = None

        return cls(
            autor_id=data.get('autor_id', ''),
            nombre=data.get('nombre', ''),
            ruta_imagen=data.get('ruta_imagen', ''),
            grado_academico=data.get('grado_academico', []),
            _id=_id
        )

