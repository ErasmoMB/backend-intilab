import requests
import certifi
import hashlib
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

    def _fix_encoding(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return text or ""
        try:
            return text.encode("latin-1").decode("utf-8")
        except Exception:
            return text

    def buscar_autores(self, author_ids: List[str], use_cache: bool = True, names_map: Optional[Dict[str, Dict[str, str]]] = None) -> List[Dict[str, Any]]:
        cache_key = f"autores_{'_'.join(sorted(author_ids))}"
        
        if use_cache:
            cached_data = load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        
        try:
            headers = self._get_headers()
            resultados = []
            
            for author_id in author_ids:
                url = f"{self.BASE_URL}/content/search/scopus"
                params = {"query": f"AU-ID({author_id})", "count": 1}
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                sr = data.get("search-results", {})
                entry = sr.get("entry", []) or []
                first_entry = entry[0] if isinstance(entry, list) and entry else {}
                total_docs = int(first_entry.get("document-count", sr.get("opensearch:totalResults", 0)) or 0)
                subject_area = first_entry.get("subject-area", []) or []

                surname = ""
                given_name = ""
                if names_map and author_id in names_map:
                    surname = self._fix_encoding(names_map[author_id].get("surname", ""))
                    given_name = self._fix_encoding(names_map[author_id].get("given-name", ""))
                
                resultados.append({
                    "dc:identifier": f"AUTHOR_ID:{author_id}",
                    "preferred-name": {"surname": surname, "given-name": given_name},
                    "document-count": str(total_docs),
                    "cited-by-count": "0",
                    "subject-area": subject_area,
                })
            
            if use_cache:
                save_to_cache(cache_key, resultados)
            
            return resultados
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en buscar_autores: {e}")
            raise APIException(f"Error al buscar autores: {str(e)}")

    def buscar_autores_por_ids(self, author_ids: List[str], use_cache: bool = True, names_map: Optional[Dict[str, Dict[str, str]]] = None) -> Dict[str, Dict[str, str]]:
        cache_key = f"autores_ids_{'_'.join(sorted(author_ids))}"
        
        if use_cache:
            cached_data = load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        
        headers = self._get_headers()
        autores = {}
        
        for author_id in author_ids:
            try:
                name = ""
                if names_map and author_id in names_map:
                    g = self._fix_encoding(names_map[author_id].get("given-name", ""))
                    s = self._fix_encoding(names_map[author_id].get("surname", ""))
                    name = f"{g} {s}".strip()
                else:
                    url = f"{self.BASE_URL}/content/search/scopus"
                    params = {"query": f"AU-ID({author_id})", "count": 1}
                    response = requests.get(url, headers=headers, params=params)
                    response.raise_for_status()
                    data = response.json()
                    entries = data.get("search-results", {}).get("entry", [])
                    for entry in entries:
                        creator = entry.get("dc:creator", "")
                        if creator:
                            name = creator.rstrip(".").strip()
                            break
                
                autores[author_id] = {"name": name}
            except requests.exceptions.RequestException as e:
                logger.error(f"Error en buscar_autores_por_ids para {author_id}: {e}")
                autores[author_id] = {"error": str(e)}
        
        if use_cache:
            save_to_cache(cache_key, autores)
        
        return autores

    def buscar_autores_uch(self, use_cache: bool = True) -> Dict[str, Any]:
        try:
            from src.services.institucion_service import institucion_service
            from src.models.institucion import DEFAULT_UCH_CONFIG
            afiliacion_ids = institucion_service.obtener_ids_afiliacion()
            primary_af_id = afiliacion_ids[0] if afiliacion_ids else DEFAULT_UCH_CONFIG['afiliacion_ids'][0]
        except Exception:
            from src.models.institucion import DEFAULT_UCH_CONFIG
            primary_af_id = DEFAULT_UCH_CONFIG['afiliacion_ids'][0]
        
        cache_key = f"autores_institucion_{primary_af_id}"
        
        if use_cache:
            cached_data = load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        
        try:
            headers = self._get_headers()
            autores_map = {}
            offset = 0
            count = 25
            
            url_total = f"{self.BASE_URL}/content/search/scopus?query=AF-ID({primary_af_id})&count=0"
            response_total = requests.get(url_total, headers=headers)
            response_total.raise_for_status()
            total_docs = int(response_total.json().get("search-results", {}).get("opensearch:totalResults", 0))
            
            while offset < min(total_docs, 200):
                url = f"{self.BASE_URL}/content/search/scopus?query=AF-ID({primary_af_id})&count={count}&start={offset}"
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                entries = data.get("search-results", {}).get("entry", [])
                
                for entry in entries:
                    creator = entry.get("dc:creator", "")
                    if creator:
                        name_key = creator.rstrip(".").strip()
                        if name_key not in autores_map:
                            parts = name_key.split(", ", 1)
                            if len(parts) == 2:
                                surname = parts[0]
                                given_name = parts[1]
                            else:
                                surname = ""
                                given_name = name_key
                            fake_id = hashlib.md5(name_key.encode()).hexdigest()[:11]
                            autores_map[name_key] = {
                                "dc:identifier": f"AUTHOR_ID:{fake_id}",
                                "preferred-name": {"surname": surname, "given-name": given_name},
                                "document-count": "0",
                                "cited-by-count": "0",
                                "subject-area": []
                            }
                        autores_map[name_key]["document-count"] = str(int(autores_map[name_key]["document-count"]) + 1)
                        cited = int(entry.get("citedby-count", 0) or 0)
                        autores_map[name_key]["cited-by-count"] = str(int(autores_map[name_key]["cited-by-count"]) + cited)
                
                offset += count
            
            resultados = {
                'total_autores_uch': len(autores_map),
                'autores': list(autores_map.values())
            }
            
            if use_cache:
                save_to_cache(cache_key, resultados)
            
            return resultados
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en buscar_autores_uch: {e}")
            raise APIException(f"Error al buscar autores de la institución: {str(e)}")

    def buscar_documentos(self, au_id: str, use_cache: bool = True) -> List[Dict[str, Any]]:
        cache_key = f"documentos_{au_id}"
        
        if use_cache:
            cached_data = load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        headers = self._get_headers()
        documentos = []
        count = 25
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
            headers = self._get_headers()
            url = f"{self.BASE_URL}/content/search/scopus?query=AF-ID({af_id})"
            response = requests.get(url, headers=headers)
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
            url = f"{self.BASE_URL}/content/search/scopus?query={afid_query}"
            
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

