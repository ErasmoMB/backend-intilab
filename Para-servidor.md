from flask import Blueprint, jsonify, request
import os
import json
from .autores import buscar_autores
from .documentos import buscar_documentos
from .documentos_afiliados import buscar_documentos_afiliacion
from .autorid import buscar_autores_por_ids
from .uch import obtener_informacion_afiliaciones
from .autores_uch import buscar_autores_uch
from config import usuarios_collection

bp = Blueprint('routes', __name__)

def guardar_datos_localmente(nombre_archivo, datos):
    file_path = os.path.join(os.path.dirname(__file__), nombre_archivo)
    with open(file_path, 'w') as file:
        json.dump(datos, file, indent=4)

def cargar_datos_localmente(nombre_archivo):
    file_path = os.path.join(os.path.dirname(__file__), nombre_archivo)
    with open(file_path, 'r') as file:
        return json.load(file)

@bp.route('/autores', methods=['GET'])
def autores_route():
    try:
        author_ids = ["57210377414", "57225097710", "57203357446", "58562875900", "57205596738", "56741286500", "57211666738", "57207915215", "57215928001", "57215218631", "58127854500", "57223372908", "15750919900", "57209658640", "57205765369", "57364197600", "57016156500", "58077315000", "36659719000", "58886913200"]
        autores = buscar_autores(author_ids)
        guardar_datos_localmente('autores.json', autores)
        return jsonify({"autores": autores})
    except Exception as e:
        try:
            autores = cargar_datos_localmente('autores.json')
            return jsonify({"autores": autores})
        except Exception as file_error:
            return jsonify({"error": str(file_error)}), 500

@bp.route('/autor', methods=['GET'])
def autor_route():
    try:
        author_ids = ["57210377414", "57225097710", "57203357446", "58562875900", "57205596738", "56741286500", "57211666738", "57207915215", "57215928001", "57215218631", "58127854500", "57223372908", "15750919900", "57209658640", "57205765369", "57364197600", "57016156500", "58077315000", "36659719000", "58886913200"]
        autores = buscar_autores_por_ids(author_ids)
        guardar_datos_localmente('autor.json', autores)
        return jsonify({"autores": autores})
    except Exception as e:
        try:
            autores = cargar_datos_localmente('autor.json')
            return jsonify({"autores": autores})
        except Exception as file_error:
            return jsonify({"error": str(file_error)}), 500

@bp.route('/documentos', methods=['GET'])
def get_documentos():
    author_ids = [
        "57210377414", "57225097710", "57203357446", "58562875900", "57205596738",
        "56741286500", "57211666738", "57207915215", "57215928001", "57215218631",
        "58127854500", "57223372908", "15750919900", "57209658640", "57205765369",
        "57364197600", "57016156500", "58077315000", "36659719000", "58886913200"
    ]

    try:
        documentos = {}
        for au_id in author_ids:
            documentos[au_id] = buscar_documentos(au_id)
        guardar_datos_localmente('documentos.json', documentos)
        return jsonify({'documentos': documentos})
    except Exception as e:
        try:
            documentos = cargar_datos_localmente('documentos.json')
            return jsonify({'documentos': documentos})
        except Exception as file_error:
            return jsonify({"error": str(file_error)}), 500

@bp.route('/e-health', methods=['GET'])
def get_e_health_documents():
    try:
        documentos = buscar_documentos_afiliacion("60171643")
        guardar_datos_localmente('e_health.json', documentos)
        return jsonify({"documentos": documentos})
    except Exception as e:
        try:
            documentos = cargar_datos_localmente('e_health.json')
            return jsonify({"documentos": documentos})
        except Exception as file_error:
            return jsonify({"error": str(file_error)}), 500

@bp.route('/ciics', methods=['GET'])
def get_ciics_documents():
    try:
        documentos = buscar_documentos_afiliacion("60171638")
        guardar_datos_localmente('ciics.json', documentos)
        return jsonify({"documentos": documentos})
    except Exception as e:
        try:
            documentos = cargar_datos_localmente('ciics.json')
            return jsonify({"documentos": documentos})
        except Exception as file_error:
            return jsonify({"error": str(file_error)}), 500

@bp.route('/inti-lab', methods=['GET'])
def get_inti_lab_documents():
    try:
        documentos = buscar_documentos_afiliacion("60171637")
        guardar_datos_localmente('inti_lab.json', documentos)
        return jsonify({"documentos": documentos})
    except Exception as e:
        try:
            documentos = cargar_datos_localmente('inti_lab.json')
            return jsonify({"documentos": documentos})
        except Exception as file_error:
            return jsonify({"error": str(file_error)}), 500
    
@bp.route('/datos', methods=['GET'])
def datos_investigadores():
    try:
        investigadores = list(usuarios_collection.find())
        for investigador in investigadores:
            investigador['_id'] = str(investigador['_id'])
        guardar_datos_localmente('datos_investigadores.json', investigadores)
        return jsonify(investigadores), 200
    except Exception as e:
        try:
            investigadores = cargar_datos_localmente('datos_investigadores.json')
            return jsonify(investigadores), 200
        except Exception as file_error:
            return jsonify({'error': str(file_error)}), 500
    
@bp.route('/uch', methods=['GET'])
def get_uch_information():
    institucion_ids = [
        "60110778",  # Universidad de Ciencias y Humanidades
        "60171637",  # Centro de Investigación E-Health
        "60171638",  # Centro de Investigación Interdisciplinar Ciencia y Sociedad
        "60171647",  # Estudios Generales
        "60171644",  # Facultad de Ciencias Contables Económicas y Financieras
        "60171645",  # Facultad de Ciencias de la Salud
        "60171646",  # Facultad de Humanidades y Ciencias Sociales
        "60171643"   # Image Processing Research Laboratory
    ]

    try:
        # Obtén la información utilizando los IDs predefinidos
        informacion = obtener_informacion_afiliaciones(institucion_ids)
        guardar_datos_localmente('informacion_uch.json', informacion)
        return jsonify({
            "informacion_afiliaciones": informacion  # Incluye la información adicional si es necesario
        })
    except Exception as e:
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
        resultados = buscar_autores_uch()
        guardar_datos_localmente('autores_uch.json', resultados)
        return jsonify(resultados)
    except Exception as e:
        try:
            resultados = cargar_datos_localmente('autores_uch.json')
            return jsonify(resultados)
        except Exception as file_error:
            return jsonify({"error": str(file_error)}), 500