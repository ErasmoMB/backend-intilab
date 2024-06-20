from flask import Flask, render_template
from flask_cors import CORS
from src.routes.routes import bp as routes_bp  # Importa el Blueprint
import os

# Obtén la ruta absoluta del directorio actual
dir_path = os.path.dirname(os.path.realpath(__file__))

# Crea la aplicación Flask
app = Flask(__name__,
            template_folder=os.path.join(dir_path, './src/templates'),
            static_folder=os.path.join(dir_path, './src/static'))

# Habilita CORS
CORS(app)

# Registra el Blueprint
app.register_blueprint(routes_bp)

# Ruta para la página de inicio
@app.route('/')
def home():
    return render_template('index.html')

# Punto de entrada para ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
