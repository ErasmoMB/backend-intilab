from pymongo import MongoClient
from pymongo.database import Database as MongoDatabase
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import Optional
from src.config.settings import config
from src.utils.logger import logger

class Database:
    _client: Optional[MongoClient] = None
    _db: Optional[MongoDatabase] = None
    _collection: Optional[Collection] = None

    @classmethod
    def connect(cls) -> Optional[MongoClient]:
        if cls._client is not None:
            return cls._client
        
        mongodb_uri = config.mongodb_uri_or_none
        if not mongodb_uri:
            logger.warning("MONGODB_URI no está configurado")
            return None
        
        try:
            cls._client = MongoClient(
                mongodb_uri,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            cls._client.admin.command('ping')
            cls._db = cls._client.get_database(config.MONGODB_DB_NAME)
            cls._collection = cls._db[config.MONGODB_COLLECTION]
            logger.info("Conexión a MongoDB establecida correctamente")
            return cls._client
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Error al conectar con MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al conectar con MongoDB: {e}")
            raise

    @classmethod
    def get_collection(cls) -> Collection:
        if cls._collection is None:
            cls.connect()
        if cls._collection is None:
            raise ConnectionError("No se pudo establecer conexión con MongoDB")
        return cls._collection

    @classmethod
    def get_db(cls) -> Optional[MongoDatabase]:
        if cls._db is None:
            cls.connect()
        return cls._db

    @classmethod
    def close(cls) -> None:
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            cls._collection = None

db = Database()

