from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from src.config.settings import config
from src.utils.logger import logger

class Database:
    _client = None
    _db = None
    _collection = None

    @classmethod
    def connect(cls):
        if cls._client is None:
            if not config.MONGODB_URI:
                logger.warning("MONGODB_URI no está configurado. La conexión a MongoDB no se establecerá.")
                return None
            try:
                cls._client = MongoClient(
                    config.MONGODB_URI,
                    serverSelectionTimeoutMS=5000
                )
                cls._client.admin.command('ping')
                cls._db = cls._client.get_database(config.MONGODB_DB_NAME)
                cls._collection = cls._db[config.MONGODB_COLLECTION]
                logger.info("Conexión a MongoDB establecida correctamente")
            except ConnectionFailure as e:
                logger.error(f"Error al conectar con MongoDB: {e}")
                raise
            except Exception as e:
                logger.error(f"Error inesperado al conectar con MongoDB: {e}")
                raise
        return cls._client

    @classmethod
    def get_collection(cls):
        if cls._collection is None:
            cls.connect()
        if cls._collection is None:
            raise ConnectionError("No se pudo establecer conexión con MongoDB. Verifica MONGODB_URI en .env")
        return cls._collection

    @classmethod
    def get_db(cls):
        if cls._db is None:
            cls.connect()
        return cls._db

    @classmethod
    def close(cls):
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            cls._collection = None

db = Database()

