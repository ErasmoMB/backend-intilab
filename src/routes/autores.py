from flask import jsonify
import requests
from config import API_KEY

def buscar_autores():
    url = 'https://api.elsevier.com/content/search/author'
    params = {'apiKey': API_KEY, 'query': 'AF-ID(60110778)'}

    response = requests.get(url, params=params, verify=False)
    data = response.json()

    total_resultados = int(data["search-results"]["opensearch:totalResults"])

    return total_resultados
