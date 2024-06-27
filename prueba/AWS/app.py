import os
import boto3
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

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

# Configuración de subida
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    response = s3.list_objects_v2(Bucket=S3_BUCKET)
    if 'Contents' in response:
        images = [get_s3_url(file['Key']) for file in response['Contents']]
    else:
        images = []
    return render_template('index.html', images=images, bucket=S3_BUCKET, region=S3_REGION)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Subir el archivo directamente a S3
        try:
            s3.upload_fileobj(
                file,
                S3_BUCKET,
                filename,
                ExtraArgs={'ACL': 'public-read'}
            )
            return redirect(url_for('index'))
        except Exception as e:
            return "Error al subir el archivo a S3: " + str(e), 400
    else:
        return "Archivo no permitido", 400

def get_s3_url(file_key):
    """ Función para construir la URL de la imagen en S3 """
    return f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file_key}"

if __name__ == '__main__':
    app.run(debug=True)
