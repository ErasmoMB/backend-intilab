""" API_KEY = '586c26d9a0fc3f6ab3e9a9f3b0e68eb0' """
""" API_KEY = '70c3c7f627b46b8e8d0e843c93ea15b6' """
""" API_KEY = '128e2766eb81861d19ac543e6ad30c24' """
API_KEY = '70c3c7f627b46b8e8d0e843c93ea15b6'
# config.py
import os
import logging
from pymongo import MongoClient
import boto3

# Configura el registro de errores
logging.basicConfig(filename='app.log', level=logging.ERROR)

# Configuraciones de AWS
S3_BUCKET = 'se-autores'
S3_REGION = 'us-east-1'
AWS_ACCESS_KEY_ID = 'AKIA4IP2CSAVE4HZGQAW'
AWS_SECRET_ACCESS_KEY = '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'

try:
    # Configurar el cliente de S3
    s3 = boto3.client(
        's3',
        region_name=S3_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
except Exception as e:
    logging.error(f"Error al configurar cliente de AWS S3: {e}")

# Configuraciones de MongoDB
URI = "mongodb+srv://ErasmoMB:72843381@clusteruch.7r7hbb6.mongodb.net/InvestigadoresUch"

try:
    client = MongoClient(URI)
    db = client.get_database('InvestigadoresUch')
    usuarios_collection = db.investigadores
except Exception as e:
    logging.error(f"Error al conectar con MongoDB: {e}")

# Configuración de subida
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
