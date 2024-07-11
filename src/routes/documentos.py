import requests
import logging
from config import API_KEY

# Configura el registro de errores
logging.basicConfig(filename='app.log', level=logging.ERROR)

def buscar_documentos(au_id):
    headers = {"X-ELS-APIKey": API_KEY}
    documentos = {}

    try:
        url = f"https://api.elsevier.com/content/search/scopus?query=AU-ID({au_id})&count=100"
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        data = response.json()
        documentos = data.get("search-results", {}).get("entry", [])

    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException en buscar_documentos para AU-ID {au_id}: {e}")
        documentos = {"error": str(e)}

    except Exception as e:
        logging.error(f"Error inesperado en buscar_documentos para AU-ID {au_id}: {e}")
        documentos = {"error": str(e)}

    return documentos
