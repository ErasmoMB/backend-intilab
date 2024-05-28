import requests
from config import API_KEY
import xmltodict

def buscar_autores_por_ids(author_ids):
    headers = {"X-ELS-APIKey": API_KEY}
    autores = {}

    for author_id in author_ids:
        url = f"https://api.elsevier.com/content/author/author_id/{author_id}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            autores[author_id] = {"error": f"La API devolvió un error con el código de estado {response.status_code}"}
            continue
        
        try:
            data = xmltodict.parse(response.content)
            given_name = data['author-retrieval-response']['author-profile']['preferred-name']['given-name']
            surname = data['author-retrieval-response']['author-profile']['preferred-name']['surname']
            full_name = given_name + ' ' + surname
        except (ValueError, KeyError):
            autores[author_id] = {"error": "La API devolvió una respuesta no válida o faltan campos en la respuesta"}
            continue

        autores[author_id] = {"name": full_name}

    return autores