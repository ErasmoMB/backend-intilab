import requests
import time
import xmltodict
import certifi
from typing import List, Dict, Any, Optional
from src.config.settings import config
from src.utils.logger import logger
from src.utils.exceptions import APIException
from src.utils.cache import save_to_cache, load_from_cache

class ScopusService:
    BASE_URL = "https://api.elsevier.com"
    MAX_RETRIES = 5
    BASE_WAIT_TIME = 5

    def _get_headers(self):
        return {"X-ELS-APIKey": config.SCOPUS_API_KEY}

    def _get_params(self, query):
        return {"apiKey": config.SCOPUS_API_KEY, "query": query}

    def buscar_autores(self, author_ids: List[str], use_cache: bool = True) -> List[Dict[str, Any]]:
        cache_key = f"autores_{'_'.join(sorted(author_ids))}"
        
        if use_cache:
            cached_data = load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        
        try:
            url = f"{self.BASE_URL}/content/search/author"
            query_ids = " OR ".join([f"au-id({id})" for id in author_ids])
            params = self._get_params(query_ids)
            
            response = requests.get(url, params=params, verify=True)
            response.raise_for_status()
            data = response.json()
            
            resultados = data.get("search-results", {}).get("entry", [])
            
            if use_cache:
                save_to_cache(cache_key, resultados)
            
            return resultados
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en buscar_autores: {e}")
            raise APIException(f"Error al buscar autores: {str(e)}")

    def buscar_autores_por_ids(self, author_ids: List[str], use_cache: bool = True) -> Dict[str, Dict[str, str]]:
        cache_key = f"autores_ids_{'_'.join(sorted(author_ids))}"
        
        if use_cache:
            cached_data = load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        headers = self._get_headers()
        autores = {}
        
        for author_id in author_ids:
            url = f"{self.BASE_URL}/content/author/author_id/{author_id}"
            retries = 0
            
            while retries < self.MAX_RETRIES:
                try:
                    response = requests.get(url, headers=headers)
                    
                    if response.status_code == 200:
                        data = xmltodict.parse(response.content)
                        profile = data.get('author-retrieval-response', {}).get('author-profile', {})
                        preferred_name = profile.get('preferred-name', {})
                        given_name = preferred_name.get('given-name', '')
                        surname = preferred_name.get('surname', '')
                        full_name = f"{given_name} {surname}".strip()
                        autores[author_id] = {"name": full_name}
                        break
                    
                    elif response.status_code == 429:
                        logger.warning(f"429 Too Many Requests para el autor {author_id}. Reintentando...")
                        retries += 1
                        wait_time = self.BASE_WAIT_TIME * (2 ** (retries - 1))
                        time.sleep(wait_time)
                        continue
                    
                    else:
                        autores[author_id] = {
                            "error": f"La API devolvió un error con el código de estado {response.status_code}"
                        }
                        break
                
                except requests.exceptions.RequestException as e:
                    logger.error(f"RequestException en buscar_autores_por_ids para el autor {author_id}: {e}")
                    autores[author_id] = {"error": str(e)}
                    break
                except Exception as e:
                    logger.error(f"Error inesperado en buscar_autores_por_ids para el autor {author_id}: {e}")
                    autores[author_id] = {"error": str(e)}
                    break
            
            if retries == self.MAX_RETRIES:
                autores[author_id] = {"error": "Se alcanzó el número máximo de reintentos para este autor."}
        
        if use_cache:
            save_to_cache(cache_key, autores)
        
        return autores

    def buscar_autores_uch(self, use_cache: bool = True) -> Dict[str, Any]:
        cache_key = "autores_uch"
        
        if use_cache:
            cached_data = load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        
        try:
            url = f"{self.BASE_URL}/content/search/author"
            params = {
                'apiKey': config.SCOPUS_API_KEY,
                'query': 'AF-ID(60110778)',
                'count': 100
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            total_resultados = int(data.get("search-results", {}).get("opensearch:totalResults", 0))
            autores = data.get("search-results", {}).get("entry", [])
            
            resultados = {
                'total_autores_uch': total_resultados,
                'autores': autores
            }
            
            if use_cache:
                save_to_cache(cache_key, resultados)
            
            return resultados
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en buscar_autores_uch: {e}")
            raise APIException(f"Error al buscar autores UCH: {str(e)}")

    def buscar_documentos(self, au_id: str, use_cache: bool = True) -> List[Dict[str, Any]]:
        cache_key = f"documentos_{au_id}"
        
        if use_cache:
            cached_data = load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        headers = self._get_headers()
        documentos = []
        count = 100
        offset = 0
        
        try:
            url_total = f"{self.BASE_URL}/content/search/scopus?query=AU-ID({au_id})&count=0"
            response_total = requests.get(url_total, headers=headers)
            response_total.raise_for_status()
            total_data = response_total.json()
            total_documentos = int(total_data.get("search-results", {}).get("opensearch:totalResults", 0))
            
            while offset < total_documentos:
                url = f"{self.BASE_URL}/content/search/scopus?query=AU-ID({au_id})&count={count}&start={offset}"
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                
                if 'search-results' in data and 'entry' in data['search-results']:
                    entries = data['search-results']['entry']
                    if isinstance(entries, list):
                        documentos.extend(entries)
                    else:
                        logger.warning(f"Se esperaba una lista de documentos, pero se recibió: {entries}")
                else:
                    logger.warning(f"No se encontraron documentos para AU-ID {au_id}.")
                    break
                
                offset += count
        
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException en buscar_documentos para AU-ID {au_id}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error inesperado en buscar_documentos para AU-ID {au_id}: {e}")
            return []
        
        if use_cache:
            save_to_cache(cache_key, documentos)
        
        return documentos

    def buscar_documentos_afiliacion(self, af_id: str, use_cache: bool = True) -> tuple[List[Dict[str, Any]], int]:
        cache_key = f"documentos_afiliacion_{af_id}"
        
        if use_cache:
            cached_data = load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data, 200
        
        try:
            url = f"{self.BASE_URL}/content/search/scopus?query=AF-ID({af_id})&APIKey={config.SCOPUS_API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            documentos = data.get('search-results', {}).get('entry', [])
            
            if use_cache:
                save_to_cache(cache_key, documentos)
            
            return documentos, response.status_code
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en buscar_documentos_afiliacion para AF-ID {af_id}: {e}")
            raise APIException(f"Error al buscar documentos de afiliación: {str(e)}")

    def obtener_informacion_afiliaciones(self, institucion_ids: List[str], use_cache: bool = True) -> Dict[str, Any]:
        cache_key = f"afiliaciones_{'_'.join(sorted(institucion_ids))}"
        
        if use_cache:
            cached_data = load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        
        try:
            afid_query = " OR ".join([f"AF-ID({afid})" for afid in institucion_ids])
            url = f"{self.BASE_URL}/content/search/scopus?query={afid_query}&apiKey={config.SCOPUS_API_KEY}"
            
            headers = self._get_headers()
            response = requests.get(url, headers=headers, verify=certifi.where())
            response.raise_for_status()
            
            resultados = response.json()
            
            if use_cache:
                save_to_cache(cache_key, resultados)
            
            return resultados
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException en obtener_informacion_afiliaciones: {e}")
            return {"error": str(e)}
        except Exception as e:
            logger.error(f"Error inesperado en obtener_informacion_afiliaciones: {e}")
            return {"error": str(e)}

scopus_service = ScopusService()

