import os
import boto3
from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS

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

@app.route('/')
def index():
    investigadores = list(usuarios_collection.find())
    for investigador in investigadores:
        investigador['_id'] = str(investigador['_id'])
    return render_template('index.html', investigadores=investigadores)

@app.route('/datos', methods=['GET'])
def datos_investigadores():
    try:
        investigadores = list(usuarios_collection.find())
        for investigador in investigadores:
            investigador['_id'] = str(investigador['_id'])
        return jsonify(investigadores), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    CORS(app)
    app.run(debug=True, port=2000)
