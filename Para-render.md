from flask import Blueprint, jsonify, request
import os
import json
from config import usuarios_collection

bp = Blueprint('routes', __name__)

def cargar_datos_localmente(nombre_archivo):
    file_path = os.path.join(os.path.dirname(__file__), nombre_archivo)
    with open(file_path, 'r') as file:
        return json.load(file)

@bp.route('/autores', methods=['GET'])
def autores_route():
    try:
        autores = cargar_datos_localmente('autores.json')
        return jsonify({"autores": autores})
    except Exception as file_error:
        return jsonify({"error": str(file_error)}), 500

@bp.route('/autor', methods=['GET'])
def autor_route():
    try:
        autores = cargar_datos_localmente('autor.json')
        return jsonify({"autores": autores})
    except Exception as file_error:
        return jsonify({"error": str(file_error)}), 500

@bp.route('/documentos', methods=['GET'])
def get_documentos():
    try:
        documentos = cargar_datos_localmente('documentos.json')
        return jsonify({'documentos': documentos})
    except Exception as file_error:
        return jsonify({"error": str(file_error)}), 500

@bp.route('/e-health', methods=['GET'])
def get_e_health_documents():
    try:
        documentos = cargar_datos_localmente('e_health.json')
        return jsonify({"documentos": documentos})
    except Exception as file_error:
        return jsonify({"error": str(file_error)}), 500

@bp.route('/ciics', methods=['GET'])
def get_ciics_documents():
    try:
        documentos = cargar_datos_localmente('ciics.json')
        return jsonify({"documentos": documentos})
    except Exception as file_error:
        return jsonify({"error": str(file_error)}), 500

@bp.route('/inti-lab', methods=['GET'])
def get_inti_lab_documents():
    try:
        documentos = cargar_datos_localmente('inti_lab.json')
        return jsonify({"documentos": documentos})
    except Exception as file_error:
        return jsonify({"error": str(file_error)}), 500

@bp.route('/datos', methods=['GET'])
def datos_investigadores():
    try:
        investigadores = cargar_datos_localmente('datos_investigadores.json')
        return jsonify(investigadores), 200
    except Exception as file_error:
        return jsonify({'error': str(file_error)}), 500

@bp.route('/uch', methods=['GET'])
def get_uch_information():
    try:
        informacion = cargar_datos_localmente('informacion_uch.json')
        return jsonify({
            "informacion_afiliaciones": informacion
        })
    except Exception as file_error:
        return jsonify({"error": str(file_error)}), 500

@bp.route('/autores-uch', methods=['GET'])
def obtener_autores_uch():
    try:
        resultados = cargar_datos_localmente('autores_uch.json')
        return jsonify(resultados)
    except Exception as file_error:
        return jsonify({"error": str(file_error)}), 500