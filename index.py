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

# Punto de entrada para ejecutar la aplicación
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)