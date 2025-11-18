from fastapi import Depends, HTTPException, Header
from typing import Optional
from src.utils.exceptions import UnauthorizedError
from src.config.settings import config

async def get_current_admin(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token de autorización requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(
                status_code=401,
                detail="Formato de autorización inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Formato de autorización inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not token or token != config.SECRET_KEY:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"authenticated": True}
