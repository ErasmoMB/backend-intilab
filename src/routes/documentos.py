import logging
from flask import jsonify
import requests
from config import API_KEY


# Configura el registro de errores
logging.basicConfig(filename='app.log', level=logging.ERROR)

def buscar_documentos():
    try:
        # Consulta para obtener el total de documentos de toda la institución
        allInstitutionsAFIDs = [
            "60110778",  # Universidad de Ciencias y Humanidades
            "60171637",  # Centro de Investi gación E-Health
            "60171638",  # Centro de Investigación Interdisciplinar Ciencia y Sociedad
            "60171647",  # Estudios Generales
            "60171644",  # Facultad de Ciencias Contables Económicas y Financieras
            "60171645",  # Facultad de Ciencias de la Salud
            "60171646",  # Facultad de Humanidades y Ciencias Sociales
            "60171643"   # Image Processing Research Laboratory
        ]

        afidQuery = " OR ".join([f"AF-ID({afid})" for afid in allInstitutionsAFIDs])

        allDocsUrl = f"https://api.elsevier.com/content/search/scopus?query={afidQuery}&count=100&APIKey={API_KEY}"

        response = requests.get(allDocsUrl, verify=True)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

        allDocsResult = response.json()

        if allDocsResult.get("search-results") and allDocsResult["search-results"].get("entry"):
            allDocs = allDocsResult["search-results"]["entry"]
            return allDocs
        else:
            return jsonify({"error": "No se pudieron obtener los documentos correctamente"})
    
    except requests.exceptions.RequestException as e:
        # Log the error using logging
        logging.error(f"Error al hacer la solicitud HTTP: {e}")
        return jsonify({"error": "Error al obtener los documentos. Inténtelo de nuevo más tarde."})

    except Exception as e:
        # Log any other unexpected errors
        logging.error(f"Error inesperado: {e}")
        return jsonify({"error": "Se produjo un error inesperado. Contacte al administrador."})
