from flask import Blueprint, jsonify, request
from .autores import buscar_autores
from .documentos import buscar_documentos
from .documentos_afiliados import buscar_documentos_afiliacion
from .autorid import buscar_autores_por_ids

bp = Blueprint('routes', __name__)

@bp.route('/autores', methods=['GET'])
def autores_route():
    try:
        autores = buscar_autores()
        return jsonify({"autores": autores})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/autor', methods=['GET'])
def autor_route():
    try:
        author_ids = ["57210377414", "57225097710", "57203357446", "58562875900", "57205596738", "56741286500", "57211666738", "57207915215", "57215928001", "57215218631", "58127854500", "57223372908", "15750919900", "57209658640", "57205765369", "57364197600", "57016156500", "58077315000", "36659719000", "58886913200"]
        autores = buscar_autores_por_ids(author_ids)
        return jsonify({"autores": autores})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/documentos', methods=['GET'])
def get_documentos():
    try:
        documentos = buscar_documentos()
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