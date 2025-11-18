import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SCOPUS_API_KEY = os.getenv('SCOPUS_API_KEY')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    S3_BUCKET = os.getenv('S3_BUCKET', 'se-autores')
    S3_REGION = os.getenv('S3_REGION', 'us-east-1')
    MONGODB_URI = os.getenv('MONGODB_URI') or None
    MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME', 'InvestigadoresUch')
    MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'investigadores')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    PORT = int(os.getenv('PORT', 5000))
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD_HASH = os.getenv('ADMIN_PASSWORD_HASH')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    _cors_origins_str = os.getenv('CORS_ORIGINS', 'http://localhost:3000')
    CORS_ORIGINS = _cors_origins_str.split(',') if _cors_origins_str else ['http://localhost:3000']

config = Config()

