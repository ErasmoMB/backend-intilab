import unittest
import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from bson import ObjectId
from fastapi import UploadFile
from src.services.investigador_service import investigador_service
from src.services.scopus_service import scopus_service
from src.services.institucion_service import institucion_service
from src.services.s3_service import s3_service
from src.utils.exceptions import NotFoundError, ValidationError, APIException

class TestInvestigadorService(unittest.TestCase):
    def setUp(self):
        self.mock_collection = Mock()
        investigador_service.collection = self.mock_collection

    def test_obtener_todos(self):
        mock_data = [
            {"_id": ObjectId(), "nombre": "Test", "autor_id": "123"},
            {"_id": ObjectId(), "nombre": "Test2", "autor_id": "456"}
        ]
        self.mock_collection.find.return_value = mock_data
        result = investigador_service.obtener_todos()
        self.assertEqual(len(result), 2)
        self.assertIn("_id", result[0])

    def test_obtener_por_id_success(self):
        mock_id = ObjectId()
        mock_data = {"_id": mock_id, "nombre": "Test", "autor_id": "123"}
        self.mock_collection.find_one.return_value = mock_data
        result = investigador_service.obtener_por_id(str(mock_id))
        self.assertEqual(result["nombre"], "Test")

    def test_obtener_por_id_not_found(self):
        self.mock_collection.find_one.return_value = None
        with self.assertRaises(NotFoundError):
            investigador_service.obtener_por_id(str(ObjectId()))

    def test_obtener_por_id_invalid(self):
        with self.assertRaises(ValidationError):
            investigador_service.obtener_por_id("invalid_id")

    @patch.object(s3_service, 'upload_file', new_callable=AsyncMock)
    def test_crear_investigador(self, mock_upload_file):
        import asyncio
        
        mock_upload_file.return_value = "https://example.com/image.jpg"
        
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.jpg"
        mock_file.read = AsyncMock(return_value=b"fake_data")
        mock_file.seek = AsyncMock()
        
        self.mock_collection.insert_one.return_value = Mock(inserted_id=ObjectId())
        result = asyncio.run(investigador_service.crear(
            autor_id="123",
            nombre="Test",
            grado_academico=["PhD"],
            imagen=mock_file
        ))
        self.assertIn("_id", result)
        self.assertEqual(result["nombre"], "Test")

    def test_eliminar_success(self):
        mock_id = ObjectId()
        self.mock_collection.delete_one.return_value = Mock(deleted_count=1)
        investigador_service.eliminar(str(mock_id))
        self.mock_collection.delete_one.assert_called_once()

    def test_eliminar_not_found(self):
        self.mock_collection.delete_one.return_value = Mock(deleted_count=0)
        with self.assertRaises(NotFoundError):
            investigador_service.eliminar(str(ObjectId()))

class TestScopusService(unittest.TestCase):
    @patch('src.utils.cache.load_from_cache')
    @patch('requests.get')
    def test_buscar_autores(self, mock_get, mock_cache):
        mock_cache.return_value = None
        mock_response = Mock()
        mock_response.json.return_value = {
            "search-results": {
                "entry": [{"dc:identifier": "123", "preferred-name": {"given-name": "Test"}}]
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = scopus_service.buscar_autores(["123"], use_cache=False)
        self.assertIsInstance(result, list)

    @patch('requests.get')
    def test_buscar_documentos(self, mock_get):
        mock_response_total = Mock()
        mock_response_total.json.return_value = {
            "search-results": {"opensearch:totalResults": "10"}
        }
        mock_response_total.raise_for_status = Mock()
        
        mock_response = Mock()
        mock_response.json.return_value = {
            "search-results": {
                "entry": [{"dc:title": "Test Document"}]
            }
        }
        mock_response.raise_for_status = Mock()
        
        mock_get.side_effect = [mock_response_total, mock_response]
        
        result = scopus_service.buscar_documentos("123", use_cache=False)
        self.assertIsInstance(result, list)

class TestInstitucionService(unittest.TestCase):
    def setUp(self):
        self.mock_db = Mock()
        self.mock_collection = Mock()
        self.mock_db.__getitem__ = Mock(return_value=self.mock_collection)
        institucion_service.db = self.mock_db
        institucion_service.collection = None

    def test_obtener_configuracion_existing(self):
        mock_config = {"_id": ObjectId(), "nombre": "Test University"}
        self.mock_collection.find_one.return_value = mock_config
        result = institucion_service.obtener_configuracion()
        self.assertEqual(result["nombre"], "Test University")

    def test_obtener_configuracion_new(self):
        self.mock_collection.find_one.return_value = None
        self.mock_collection.insert_one.return_value = Mock(inserted_id=ObjectId())
        result = institucion_service.obtener_configuracion()
        self.assertIn("_id", result)

    def test_obtener_ids_afiliacion(self):
        mock_config = {"afiliacion_ids": ["123", "456"]}
        self.mock_collection.find_one.return_value = mock_config
        result = institucion_service.obtener_ids_afiliacion()
        self.assertEqual(result, ["123", "456"])

class TestS3Service(unittest.TestCase):
    @patch('src.config.s3.s3_client.get_url')
    @patch('src.config.s3.s3_client.get_client')
    def test_upload_file(self, mock_get_client, mock_get_url):
        import asyncio
        mock_client = Mock()
        mock_client.upload_fileobj = Mock()
        mock_get_client.return_value = mock_client
        mock_get_url.return_value = "https://example.com/file.jpg"
        
        mock_file = Mock(spec=UploadFile)
        mock_file.read = AsyncMock(return_value=b"fake_data")
        mock_file.seek = AsyncMock()
        
        result = asyncio.run(s3_service.upload_file(mock_file, "test.jpg"))
        self.assertEqual(result, "https://example.com/file.jpg")

if __name__ == '__main__':
    unittest.main()
