import os
from typing import List, Set
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SCOPUS_API_KEY: str = os.getenv("SCOPUS_API_KEY", "")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    S3_BUCKET: str = os.getenv("S3_BUCKET", "se-autores")
    S3_REGION: str = os.getenv("S3_REGION", "us-east-1")
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "InvestigadoresUch")
    MONGODB_COLLECTION: str = os.getenv("MONGODB_COLLECTION", "investigadores")
    FLASK_ENV: str = os.getenv("FLASK_ENV", "development")
    PORT: int = int(os.getenv("PORT", "5000"))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD_HASH: str = os.getenv("ADMIN_PASSWORD_HASH", "")
    ALLOWED_EXTENSIONS: Set[str] = {"png", "jpg", "jpeg", "gif"}
    
    def __init__(self):
        default_origins = [
            "http://localhost:3000",
            "http://localhost:3001",
            "https://frontend-intilab.onrender.com",
        ]
        cors_origins_str = os.getenv("CORS_ORIGINS", "")
        if cors_origins_str:
            env_origins = [
                origin.strip() 
                for origin in cors_origins_str.split(",") 
                if origin.strip()
            ]
            self.CORS_ORIGINS: List[str] = list(set(env_origins + default_origins))
        else:
            self.CORS_ORIGINS: List[str] = default_origins

    @property
    def mongodb_uri_or_none(self) -> str | None:
        return self.MONGODB_URI if self.MONGODB_URI else None

config = Settings()

