from flask import Blueprint, jsonify
import requests
import certifi
import logging
from config import API_KEY

# Configura el registro de errores
logging.basicConfig(filename='app.log', level=logging.ERROR)

def obtener_informacion_afiliaciones(institucion_ids):
    """
    Obtiene la información de afiliaciones de Scopus para una lista de IDs de afiliación.
    """
    afid_query = " OR ".join([f"AF-ID({afid})" for afid in institucion_ids])
    url = f"https://api.elsevier.com/content/search/scopus?query={afid_query}&apiKey={API_KEY}"

    headers = {"X-ELS-APIKey": API_KEY}
    try:
        response = requests.get(url, headers=headers, verify=certifi.where())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException en obtener_informacion_afiliaciones: {e}")
        return {"error": str(e)}
    except Exception as e:
        logging.error(f"Error inesperado en obtener_informacion_afiliaciones: {e}")
        return {"error": str(e)}