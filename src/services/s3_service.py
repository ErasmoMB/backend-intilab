from fastapi import UploadFile
from src.config.s3 import s3_client
from src.config.settings import config
from src.utils.logger import logger
from src.utils.exceptions import APIException

class S3Service:
    async def upload_file(self, file: UploadFile, filename: str) -> str:
        try:
            client = s3_client.get_client()
            file_content = await file.read()
            import io
            file_obj = io.BytesIO(file_content)
            client.upload_fileobj(
                file_obj,
                config.S3_BUCKET,
                filename,
                ExtraArgs={'ACL': 'public-read'}
            )
            url = s3_client.get_url(filename)
            logger.info(f"Archivo {filename} subido exitosamente a S3")
            await file.seek(0)
            return url
        except Exception as e:
            logger.error(f"Error al subir archivo a S3: {e}")
            raise APIException(f"Error al subir archivo: {str(e)}")

    def get_file_url(self, filename: str) -> str:
        return s3_client.get_url(filename)

s3_service = S3Service()

