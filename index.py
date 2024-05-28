from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from src.routes.routes import bp as routes_bp  # Importa el Blueprint
import os

# Obtén la ruta absoluta del directorio actual
dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__, template_folder=os.path.join(dir_path, './src/templates'), static_folder=os.path.join(dir_path, './src/static'))
CORS(app)

app.register_blueprint(routes_bp)  # Registra el Blueprint

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)