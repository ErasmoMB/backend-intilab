from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import boto3
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import requests

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuraciones de AWS
S3_BUCKET = os.getenv('S3_BUCKET')
S3_REGION = os.getenv('S3_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

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
    # Obtener lista de investigadores desde MongoDB
    investigadores = list(usuarios_collection.find())
    for investigador in investigadores:
        investigador['_id'] = str(investigador['_id'])

    # Obtener lista de autores desde la API interna
    try:
        response = requests.get('http://localhost:5000/autor')
        if response.status_code == 200:
            autores = response.json()['autores']
        else:
            autores = {}
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener autores: {e}")
        autores = {}

    return render_template('index.html', investigadores=investigadores, autores=autores)

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
            
            # Obtener grados académicos desde el formulario
            grados_academicos = request.form.getlist('grado_academico')
            autor_id = request.form.get('autor_id')  # ID del autor seleccionado

            # Guardar el nuevo investigador en MongoDB
            nuevo_investigador = {
                'nombre': request.form.get('nombre'),  # Ajusta según el nombre del campo en el formulario
                'autor_id': autor_id,
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

if __name__ == '__main__':
    app.run(debug=True, port=8000)
