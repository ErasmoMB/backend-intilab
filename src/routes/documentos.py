from flask import jsonify
import requests
from config import API_KEY

def buscar_documentos():
    # Consulta para obtener el total de documentos de toda la institución
    allInstitutionsAFIDs = [
        "60110778",  # Universidad de Ciencias y Humanidades
        "60171637",  # Centro de Investigación E-Health
        "60171638",  # Centro de Investigación Interdisciplinar Ciencia y Sociedad
        "60171647",  # Estudios Generales
        "60171644",  # Facultad de Ciencias Contables Económicas y Financieras
        "60171645",  # Facultad de Ciencias de la Salud
        "60171646",  # Facultad de Humanidades y Ciencias Sociales
        "60171643"  # Image Processing Research Laboratory
    ]

    afidQuery = " OR ".join([f"AF-ID({afid})" for afid in allInstitutionsAFIDs])

    allDocsUrl = f"https://api.elsevier.com/content/search/scopus?query={afidQuery}&count=100&APIKey={API_KEY}"

    response = requests.get(allDocsUrl, verify=True)
    allDocsResult = response.json()

    if allDocsResult["search-results"] and allDocsResult["search-results"]["entry"]:
        allDocs = allDocsResult["search-results"]["entry"]
        return allDocs
    else:
        return jsonify({"error": "No se pudieron obtener los documentos correctamente"})


