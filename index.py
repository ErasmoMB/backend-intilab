from flask import Flask, jsonify, render_template
import requests
from config import API_KEY
from src.routes.autores import buscar_autores
from src.routes.documentos import buscar_documentos, buscar_documentos_afiliacion

app = Flask(__name__)

@app.route('/')
def index():
    autores = buscar_autores()
    documentos = buscar_documentos()
    doc_afiliados = buscar_documentos_afiliacion()
    
    # Imprime los resultados en la consola para verificar
    print("Autores:", autores)
    print("Documentos:", documentos)
    print("Documentos afiliados:", doc_afiliados)
    
    return "Verifica la consola para ver los resultados"

if __name__ == '__main__':
    app.run(debug=True)
