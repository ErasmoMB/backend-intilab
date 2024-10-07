import requests
import logging
import xmltodict
from config import API_KEY
import time

# Configura el registro de errores
logging.basicConfig(filename='app.log', level=logging.ERROR)

def buscar_autores_por_ids(author_ids):
    headers = {"X-ELS-APIKey": API_KEY}
    autores = {}
    max_retries = 5  # Número máximo de reintentos para el error 429
    base_wait_time = 5  # Tiempo de espera base en segundos

    for author_id in author_ids:
        url = f"https://api.elsevier.com/content/author/author_id/{author_id}"
        retries = 0

        while retries < max_retries:
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

                if response.status_code == 200:
                    data = xmltodict.parse(response.content)
                    given_name = data['author-retrieval-response']['author-profile']['preferred-name']['given-name']
                    surname = data['author-retrieval-response']['author-profile']['preferred-name']['surname']
                    full_name = given_name + ' ' + surname
                    autores[author_id] = {"name": full_name}
                    break  # Salir del bucle si la solicitud fue exitosa

                elif response.status_code == 429:
                    logging.warning(f"429 Too Many Requests para el autor {author_id}. Reintentando...")
                    retries += 1
                    wait_time = base_wait_time * (2 ** (retries - 1))  # Espera exponencial
                    logging.info(f"Esperando {wait_time} segundos antes de reintentar...")
                    time.sleep(wait_time)  # Espera antes de reintentar
                    continue  # Volver a intentar la solicitud

                else:
                    autores[author_id] = {"error": f"La API devolvió un error con el código de estado {response.status_code}"}
                    break

            except requests.exceptions.RequestException as e:
                logging.error(f"RequestException en buscar_autores_por_ids para el autor {author_id}: {e}")
                autores[author_id] = {"error": str(e)}
                break  # Salir del bucle en caso de excepción

            except Exception as e:
                logging.error(f"Error inesperado en buscar_autores_por_ids para el autor {author_id}: {e}")
                autores[author_id] = {"error": str(e)}
                break  # Salir del bucle en caso de excepción

        # Si se alcanzó el número máximo de reintentos para el error 429
        if retries == max_retries:
            autores[author_id] = {"error": "Se alcanzó el número máximo de reintentos para este autor."}

    return autores