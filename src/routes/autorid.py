import requests
import logging
import xmltodict
from config import API_KEY

# Configura el registro de errores
logging.basicConfig(filename='app.log', level=logging.ERROR)

def buscar_autores_por_ids(author_ids):
    headers = {"X-ELS-APIKey": API_KEY}
    autores = {}

    for author_id in author_ids:
        url = f"https://api.elsevier.com/content/author/author_id/{author_id}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            if response.status_code != 200:
                autores[author_id] = {"error": f"La API devolvió un error con el código de estado {response.status_code}"}
                continue

            data = xmltodict.parse(response.content)
            given_name = data['author-retrieval-response']['author-profile']['preferred-name']['given-name']
            surname = data['author-retrieval-response']['author-profile']['preferred-name']['surname']
            full_name = given_name + ' ' + surname

            autores[author_id] = {"name": full_name}

        except requests.exceptions.RequestException as e:
            logging.error(f"RequestException en buscar_autores_por_ids para el autor {author_id}: {e}")
            autores[author_id] = {"error": str(e)}

        except Exception as e:
            logging.error(f"Error inesperado en buscar_autores_por_ids para el autor {author_id}: {e}")
            autores[author_id] = {"error": str(e)}

    return autores
