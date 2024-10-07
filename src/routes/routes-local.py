from flask import Blueprint, jsonify, request
from config import usuarios_collection
from .autores import buscar_autores
from .autores_uch import buscar_autores_uch
from .autorid import buscar_autores_por_ids
from .documentos import buscar_documentos
from .documentos_afiliados import buscar_documentos_afiliacion
from .uch import obtener_informacion_afiliaciones

bp = Blueprint('routes', __name__)

@bp.route('/autores', methods=['GET'])
def autores_route():
    try:
        author_ids = [
            "15750919900", "36659719000", "56741286500", "57016156500", 
            "57203357446", "57205596738", "57205765369", "57207915215", 
            "57209658640", "57210377414", "57211666738", "57215218631", 
            "57215928001", "57223372908", "57225097710", "57364197600", 
            "58077315000", "58127854500", "58562875900", "58886913200","57930813500","57204841219"
        ]
        autores = buscar_autores(author_ids)
        return jsonify({"autores": autores})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/autor', methods=['GET'])
def autor_route():
    try:
        author_ids = [
            "15750919900", "36659719000", "56741286500", "57016156500", 
            "57203357446", "57205596738", "57205765369", "57207915215", 
            "57209658640", "57210377414", "57211666738", "57215218631", 
            "57215928001", "57223372908", "57225097710", "57364197600", 
            "58077315000", "58127854500", "58562875900", "58886913200","57930813500","57204841219"
        ]
        autores = buscar_autores_por_ids(author_ids)
        return jsonify({"autores": autores})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/documentos', methods=['GET'])
def get_documentos():
    author_ids = [
        "57210377414", "57225097710", "57203357446", "58562875900", 
        "57205596738", "56741286500", "57211666738", "57207915215", 
        "57215928001", "57215218631", "58127854500", "57223372908", 
        "15750919900", "57209658640", "57205765369", "57364197600", 
        "57016156500", "58077315000", "36659719000", "58886913200","57930813500","57204841219"
    ]
    try:
        documentos = {}
        for au_id in author_ids:
            documentos[au_id] = buscar_documentos(au_id)
        return jsonify({'documentos': documentos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/e-health', methods=['GET'])
def get_e_health_documents():
    try:
        documentos = buscar_documentos_afiliacion("60171643")
        return jsonify({"documentos": documentos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/ciics', methods=['GET'])
def get_ciics_documents():
    try:
        documentos = buscar_documentos_afiliacion("60171638")
        return jsonify({"documentos": documentos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/inti-lab', methods=['GET'])
def get_inti_lab_documents():
    try:
        documentos = buscar_documentos_afiliacion("60171637")
        return jsonify({"documentos": documentos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
    institucion_ids = [
        "60110778",  # Universidad de Ciencias y Humanidades
        "60171637",  # Centro de Investigación E-Health
        "60171638",  # Centro de Investigación Interdisciplinar Ciencia y Sociedad
        "60171644",  # Facultad de Ciencias Contables Económicas y Financieras
        "60171645",  # Facultad de Ciencias de la Salud
        "60171646",  # Facultad de Humanidades y Ciencias Sociales
        "60171643",  # Image Processing Research Laboratory
        "60171647"   # Estudios Generales
    ]
    try:
        # Obtén la información utilizando los IDs predefinidos
        informacion = obtener_informacion_afiliaciones(institucion_ids)
        return jsonify({
            "informacion_afiliaciones": informacion  # Incluye la información adicional si es necesario
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/autores-uch', methods=['GET'])
def obtener_autores_uch():
    try:
        resultados = buscar_autores_uch()
        return jsonify(resultados)
    except Exception as e:
        return jsonify({"error": str(e)}), 500