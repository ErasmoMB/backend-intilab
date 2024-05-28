from flask import jsonify
import requests
from config import API_KEY

def buscar_documentos_afiliacion(id):
    url = f"https://api.elsevier.com/content/search/scopus?query=AF-ID({id})&apiKey=b21b68bd3eb1b573af7f883b0c9b70d7"
    response = requests.get(url)
    
    if response.status_code != 200:
        return response.json(), response.status_code

    data = response.json()
    documentos = data.get('search-results', {}).get('entry', [])
    
    return documentos, response.status_code
