from flask import Blueprint, jsonify, request
import os
import json
from config import usuarios_collection
from src.routes.autores import buscar_autores

bp = Blueprint('routes', __name__)

def cargar_datos_localmente(nombre_archivo):
    file_path = os.path.join(os.path.dirname(__file__), nombre_archivo)
    with open(file_path, 'r') as file:
        return json.load(file)

def cargar_y_devolver_datos(nombre_archivo):
    try:
        datos = cargar_datos_localmente(nombre_archivo)
        return jsonify(datos)
    except Exception as file_error:
        return jsonify({"error": str(file_error)}), 500

@bp.route('/autores', methods=['GET'])
def autores_route():
    return cargar_y_devolver_datos('autores.json')

@bp.route('/autor', methods=['GET'])
def autor_route():
    return cargar_y_devolver_datos('autor.json')

@bp.route('/documentos', methods=['GET'])
def get_documentos():
    return cargar_y_devolver_datos('documentos.json')

@bp.route('/e-health', methods=['GET'])
def get_e_health_documents():
    return cargar_y_devolver_datos('e_health.json')

@bp.route('/ciics', methods=['GET'])
def get_ciics_documents():
    return cargar_y_devolver_datos('ciics.json')

@bp.route('/inti-lab', methods=['GET'])
def get_inti_lab_documents():
    return cargar_y_devolver_datos('inti_lab.json')

@bp.route('/datos', methods=['GET'])
def datos_investigadores():
    try:
        investigadores = list(usuarios_collection.find())
        for investigador in investigadores:
            investigador['_id'] = str(investigador['_id'])
        return jsonify(investigadores), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/uch', methods=['GET'])
def get_uch_information():
    return cargar_y_devolver_datos('informacion_uch.json')

@bp.route('/autores-uch', methods=['GET'])
def obtener_autores_uch():
    return cargar_y_devolver_datos('autores_uch.json')