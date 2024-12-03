import requests
import logging
from config import API_KEY

# Configura el registro de errores
logging.basicConfig(filename='app.log', level=logging.ERROR)

def buscar_documentos(au_id):
    headers = {"X-ELS-APIKey": API_KEY}
    documentos = []
    count = 100  # Número máximo de documentos por consulta
    offset = 0

    try:
        # Primero, obtener el total de documentos
        url_total = f"https://api.elsevier.com/content/search/scopus?query=AU-ID({au_id})&count=0"
        response_total = requests.get(url_total, headers=headers)
        response_total.raise_for_status()
        total_data = response_total.json()
        
        # Asegúrate de que total_documentos sea un entero
        total_documentos = int(total_data.get("search-results", {}).get("opensearch:totalResults", 0))

        # Realizar consultas en lotes
        while offset < total_documentos:
            url = f"https://api.elsevier.com/content/search/scopus?query=AU-ID({au_id})&count={count}&start={offset}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()

            # Verificar si hay resultados
            if 'search-results' in data and 'entry' in data['search-results']:
                entries = data['search-results']['entry']
                if isinstance(entries, list):
                    documentos.extend(entries)
                else:
                    logging.error(f"Se esperaba una lista de documentos, pero se recibió: {entries}")  # Registro de error
            else:
                logging.warning(f"No se encontraron documentos para AU-ID {au_id}.")  # Registro de advertencia
                break  # Salir del bucle si no hay más documentos

            offset += count  # Incrementar el desplazamiento

    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException en buscar_documentos para AU-ID {au_id}: {e}")
        return []  # Devolver un array vacío en caso de error

    except Exception as e:
        logging.error(f"Error inesperado en buscar_documentos para AU-ID {au_id}: {e}")
        return []  # Devolver un array vacío en caso de error

    return documentos