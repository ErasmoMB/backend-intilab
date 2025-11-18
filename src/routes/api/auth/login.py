from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from src.config.settings import config

router = APIRouter(prefix='/api/auth', tags=['Auth'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    expires_in: int

@router.post('/login', response_model=LoginResponse)
async def login(data: LoginRequest):
    stored_username = config.ADMIN_USERNAME
    stored_password_hash = config.ADMIN_PASSWORD_HASH
    if not stored_password_hash:
        # Fallback ONLY for development; advises to set proper hash
        stored_password_hash = pwd_context.hash('admin')
    if data.username != stored_username or not pwd_context.verify(data.password, stored_password_hash):
        raise HTTPException(status_code=401, detail='Credenciales inválidas')
    exp_minutes = 480
    expire = datetime.utcnow() + timedelta(minutes=exp_minutes)
    payload = {
        'sub': stored_username,
        'role': 'admin',
        'exp': expire,
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
    return LoginResponse(token=token, expires_in=exp_minutes * 60)
