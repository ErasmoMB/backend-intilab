from fastapi import HTTPException, Header
from typing import Optional
from src.config.settings import config
import jwt

def _unauthorized(detail: str):
    return HTTPException(status_code=401, detail=detail, headers={"WWW-Authenticate": "Bearer"})

async def get_current_admin(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise _unauthorized("Token de autorización requerido")
    try:
        scheme, token = authorization.split()
    except ValueError:
        raise _unauthorized("Formato de autorización inválido")
    if scheme.lower() != 'bearer':
        raise _unauthorized("Formato de autorización inválido")
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])
        if payload.get('role') != 'admin':
            raise _unauthorized("Rol inválido")
    except jwt.ExpiredSignatureError:
        raise _unauthorized("Token expirado")
    except jwt.InvalidTokenError:
        raise _unauthorized("Token inválido")
    return {"authenticated": True, "user": payload.get('sub')}
