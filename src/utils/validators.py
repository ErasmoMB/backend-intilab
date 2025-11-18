import os
import re
from src.config.settings import config
from src.utils.exceptions import ValidationError

def secure_filename(filename: str) -> str:
    filename = os.path.basename(filename)
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename.strip('-_')

def allowed_file(filename):
    if '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in config.ALLOWED_EXTENSIONS

def validate_file_upload(filename: str):
    if not filename or filename == '':
        raise ValidationError("No se seleccionó ningún archivo")
    
    if not allowed_file(filename):
        raise ValidationError(
            f"Formato de archivo no permitido. Formatos permitidos: {', '.join(config.ALLOWED_EXTENSIONS)}"
        )
    
    return secure_filename(filename)

def validate_object_id(id_str):
    from bson import ObjectId
    try:
        return ObjectId(id_str)
    except Exception:
        raise ValidationError("ID inválido")

