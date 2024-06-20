

from flask import Flask, jsonify, request, render_template, url_for, send_from_directory
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Carpeta para guardar imágenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Asegúrate de usar variables de entorno para las credenciales
URI = "mongodb+srv://ErasmoMB:72843381@clusteruch.7r7hbb6.mongodb.net/InvestigadoresUch"
client = MongoClient(URI)
db = client.get_database('InvestigadoresUch')
usuarios_collection = db.investigadores

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    investigadores = list(usuarios_collection.find())
    for investigador in investigadores:
        investigador['_id'] = str(investigador['_id'])
    return render_template('index.html', investigadores=investigadores)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/investigadores', methods=['POST'])
def agregar_investigador():
    if 'imagen' not in request.files:
        return jsonify({'error': 'No se encontró el archivo de imagen'}), 400
    imagen = request.files['imagen']
    if imagen.filename == '':
        return jsonify({'error': 'No se seleccionó ninguna imagen'}), 400
    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        imagen.save(imagen_path)
        nuevo_investigador = {
            'nombre': request.form['nombre'],
            'email': request.form['email'],
            'grados_academicos': request.form.getlist('grados_academicos[]'),
            'ruta_imagen': filename  # Guarda solo el nombre del archivo para facilitar el acceso
        }
        insert_result = usuarios_collection.insert_one(nuevo_investigador)
        nuevo_investigador['_id'] = str(insert_result.inserted_id)
        return jsonify({'result': nuevo_investigador}), 201
    else:
        return jsonify({'error': 'Formato de archivo no permitido'}), 400

if __name__ == '__main__':
    app.run(debug=True)