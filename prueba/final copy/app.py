import os
import boto3
from flask import Flask, jsonify, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Configuraciones de AWS
S3_BUCKET = 'se-autores'
S3_REGION = 'us-east-1'
AWS_ACCESS_KEY_ID = 'AKIA4IP2CSAVE4HZGQAW'
AWS_SECRET_ACCESS_KEY = '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'

# Configurar el cliente de S3
s3 = boto3.client(
    's3',
    region_name=S3_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Configuraciones de MongoDB
URI = "mongodb+srv://ErasmoMB:72843381@clusteruch.7r7hbb6.mongodb.net/InvestigadoresUch"
client = MongoClient(URI)
db = client.get_database('InvestigadoresUch')
usuarios_collection = db.investigadores

# Configuración de subida
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_s3_url(file_key):
    """ Función para construir la URL de la imagen en S3 """
    return f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file_key}"

@app.route('/')
def index():
    investigadores = list(usuarios_collection.find())
    for investigador in investigadores:
        investigador['_id'] = str(investigador['_id'])
    return render_template('index.html', investigadores=investigadores)

@app.route('/investigadores', methods=['GET'])
def obtener_investigadores():
    investigadores = list(usuarios_collection.find())
    for investigador in investigadores:
        investigador['_id'] = str(investigador['_id'])
    return jsonify(investigadores)

@app.route('/investigadores/<id>', methods=['GET'])
def obtener_investigador_por_id(id):
    try:
        investigador = usuarios_collection.find_one({'_id': ObjectId(id)})
        if investigador:
            investigador['_id'] = str(investigador['_id'])
            return jsonify(investigador), 200
        else:
            return jsonify({'error': 'Investigador no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/investigadores', methods=['POST'])
def agregar_investigador():
    if 'imagen' not in request.files:
        return jsonify({'error': 'No se encontró el archivo de imagen'}), 400
    imagen = request.files['imagen']
    if imagen.filename == '':
        return jsonify({'error': 'No se seleccionó ninguna imagen'}), 400
    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        try:
            s3.upload_fileobj(
                imagen,
                S3_BUCKET,
                filename,
                ExtraArgs={'ACL': 'public-read'}
            )
            imagen_url = get_s3_url(filename)
            grados_academicos = request.form.getlist('grado_academico')
            nuevo_investigador = {
                'nombre': request.form['nombre'],
                'grado_academico': grados_academicos,
                'ruta_imagen': imagen_url  # Guarda la URL de la imagen en S3
            }
            insert_result = usuarios_collection.insert_one(nuevo_investigador)
            nuevo_investigador['_id'] = str(insert_result.inserted_id)
            return jsonify({'result': nuevo_investigador}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Formato de archivo no permitido'}), 400

@app.route('/investigadores/<id>', methods=['PUT'])
def actualizar_investigador(id):
    try:
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        grados_academicos = request.form.getlist('grado_academico')
        
        # Construir el objeto de actualización
        data = {
            'nombre': nombre,
            'grado_academico': grados_academicos
        }
        
        # Verificar si se está actualizando la imagen
        if 'imagen' in request.files:
            imagen = request.files['imagen']
            if imagen.filename != '':
                filename = secure_filename(imagen.filename)
                
                # Subir la imagen a AWS S3
                s3.upload_fileobj(
                    imagen,
                    S3_BUCKET,
                    filename,
                    ExtraArgs={'ACL': 'public-read'}
                )
                
                # Obtener la URL de la imagen en S3
                imagen_url = get_s3_url(filename)
                data['ruta_imagen'] = imagen_url

        # Actualizar el investigador en la base de datos
        result = usuarios_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        
        if result.modified_count > 0:
            return jsonify({'mensaje': 'Investigador actualizado correctamente'}), 200
        else:
            return jsonify({'error': 'No se encontró el investigador'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/investigadores/<id>', methods=['DELETE'])
def eliminar_investigador(id):
    result = usuarios_collection.delete_one({'_id': ObjectId(id)})
    
    if result.deleted_count == 1:
        return jsonify({'result': 'Investigador eliminado correctamente'}), 200
    else:
        return jsonify({'error': 'No se encontró el investigador'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=1000)
