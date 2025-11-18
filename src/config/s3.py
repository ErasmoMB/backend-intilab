import boto3
from botocore.exceptions import ClientError
from src.config.settings import config
from src.utils.logger import logger

class S3Client:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            try:
                cls._client = boto3.client(
                    's3',
                    region_name=config.S3_REGION,
                    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
                )
                logger.info("Cliente S3 configurado correctamente")
            except Exception as e:
                logger.error(f"Error al configurar cliente de AWS S3: {e}")
                raise
        return cls._client

    @classmethod
    def get_url(cls, file_key):
        return f"https://{config.S3_BUCKET}.s3.{config.S3_REGION}.amazonaws.com/{file_key}"

s3_client = S3Client()

