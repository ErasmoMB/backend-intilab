import requests
from config import API_KEY

def buscar_autores(author_ids):
    url = "https://api.elsevier.com/content/search/author"
    query_ids = " OR ".join([f"au-id({id})" for id in author_ids])
    params = {"apiKey": API_KEY, "query": query_ids}

    response = requests.get(url, params=params, verify=True)
    data = response.json()

    resultados = data["search-results"]["entry"]

    return resultados
