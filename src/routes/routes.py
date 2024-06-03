from flask import Blueprint, jsonify, request
from .autores import buscar_autores
from .documentos import buscar_documentos
from .documentos_afiliados import buscar_documentos_afiliacion
from .autorid import buscar_autores_por_ids
from ..database import create_author, get_authors, get_author, delete_author, update_author

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

@bp.route("/authors", methods=["POST"])
def create_author_route():
    id = request.form.get("id")
    image = request.files.get("image")  # La imagen es un archivo
    academic_degrees = request.form.getlist("academic_degrees")  # Los grados académicos son opcionales y pueden ser múltiples
    return create_author(id, image, academic_degrees)

@bp.route("/authors", methods=["GET"])
def get_authors_route():
    return get_authors()

@bp.route("/authors/<id>", methods=["GET"])
def get_author_route(id):
    return get_author(id)

@bp.route("/authors/<id>", methods=["DELETE"])
def delete_author_route(id):
    return delete_author(id)

@bp.route("/authors/<id>", methods=["PUT"])
def update_author_route(id):
    image = request.files.get("image", None)  # La imagen es un archivo
    academic_degrees = request.form.getlist("academic_degrees")  # Los grados académicos son opcionales y pueden ser múltiples
    return update_author(id, image, academic_degrees)