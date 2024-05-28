import requests
from config import API_KEY


def buscar_autores():
    url = "https://api.elsevier.com/content/search/author"
    params = {"apiKey": API_KEY, "query": "AF-ID(60110778)"}

    response = requests.get(url, params=params, verify=True)
    data = response.json()

    resultados = data["search-results"]["entry"]

    return resultados
