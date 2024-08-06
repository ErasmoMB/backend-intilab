import requests
from config import API_KEY

def buscar_autores_uch():
    url = 'https://api.elsevier.com/content/search/author'
    params = {'apiKey': API_KEY, 'query': 'AF-ID(60110778)', 'count': 100}

    response = requests.get(url, params=params)
    data = response.json()

    total_resultados = int(data["search-results"]["opensearch:totalResults"])
    autores = data["search-results"].get("entry", [])

    return {
        'total_autores_uch': total_resultados,
        'autores': autores
    }