from flask import Flask, request, jsonify, Response, make_response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import boto3
from botocore.exceptions import NoCredentialsError


app = Flask(__name__)
CORS(app) # Habilitando CORS
app.config["MONGO_URI"] = "mongodb://localhost/investigadoresmongodb"
mongo = PyMongo(app)

# Configuración de AWS S3
s3 = boto3.client('s3')
bucket_name = 'se-autores'  # Nombre del bucket de S3

def create_author(id, image, academic_degrees):
    if id and image:
        try:
            # Guardar la imagen en S3
            s3_filename = secure_filename(image.filename)
            s3.upload_fileobj(image, bucket_name, s3_filename)

            # Construir la URL de la imagen en S3
            s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_filename}"

            # Insertar los datos del autor en la base de datos
            result = mongo.db.authors.insert_one(
                {"_id": id, "image": s3_url, "academic_degrees": academic_degrees}
            )
            response = {
                "id": id,
                "image": s3_url,
                "academic_degrees": academic_degrees
            }
            return response
        except NoCredentialsError:
            return {"message": "No se encontraron credenciales de AWS configuradas"}
        except Exception as e:
            return {"message": f"Hubo un error al cargar la imagen a S3: {str(e)}"}
    else:
        return {"message": "Se requiere un ID y una imagen para crear un autor"}

def get_authors():
    authors = mongo.db.authors.find()
    response = json_util.dumps(authors)
    return Response(response, mimetype="application/json")

def get_author(id):
    author = mongo.db.authors.find_one({"_id": id})
    response = json_util.dumps(author)
    return Response(response, mimetype="application/json")

def delete_author(id):
    mongo.db.authors.delete_one({"_id": id})
    response = jsonify({"message": "Author " + id + " was deleted successfully"})
    return response

def update_author(id, image, academic_degrees):    
    if id and image:
        try:
            # Guardar la imagen en S3
            s3_filename = secure_filename(image.filename)
            s3.upload_fileobj(image, bucket_name, s3_filename)

            # Construir la URL de la imagen en S3
            s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_filename}"

            # Actualizar los datos del autor en la base de datos
            result = mongo.db.authors.update_one(
                {"_id": id},
                {"$set": {"image": s3_url, "academic_degrees": academic_degrees}}
            )
            if result.matched_count == 0:
                return {"message": f"No se encontró ningún autor con el ID {id}"}
            else:
                response = {
                    "id": id,
                    "image": s3_url,
                    "academic_degrees": academic_degrees
                }
                return response
        except NoCredentialsError:
            return {"message": "No se encontraron credenciales de AWS configuradas"}
        except Exception as e:
            return {"message": f"Hubo un error al cargar la imagen a S3: {str(e)}"}
    else:
        return {"message": "Se requiere un ID y una imagen para actualizar un autor"}
