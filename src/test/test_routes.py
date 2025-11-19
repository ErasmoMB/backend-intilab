import unittest
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from main import app
from src.middleware.auth import get_current_admin
from src.utils.exceptions import NotFoundError, ValidationError

class TestRoutes(unittest.TestCase):
    def setUp(self):
        from main import app
        app.dependency_overrides[get_current_admin] = lambda: {"authenticated": True, "user": "admin"}
        self.client = TestClient(app)
        self.mock_admin = {"authenticated": True, "user": "admin"}
    
    def tearDown(self):
        from main import app
        app.dependency_overrides.clear()

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    @patch('src.routes.routes.investigador_service')
    def test_datos_investigadores(self, mock_service):
        mock_service.obtener_todos.return_value = [{"nombre": "Test"}]
        response = self.client.get("/datos")
        self.assertEqual(response.status_code, 200)

    @patch('src.routes.api.admin.investigadores.investigador_service')
    def test_obtener_investigadores_admin(self, mock_service):
        mock_service.obtener_todos.return_value = [{"nombre": "Test"}]
        response = self.client.get(
            "/api/admin/investigadores",
            headers={"Authorization": "Bearer fake_token"}
        )
        self.assertEqual(response.status_code, 200)

    @patch('src.routes.api.admin.investigadores.investigador_service')
    def test_obtener_investigador_por_id(self, mock_service):
        mock_service.obtener_por_id.return_value = {"nombre": "Test", "_id": "123"}
        response = self.client.get(
            "/api/admin/investigadores/123",
            headers={"Authorization": "Bearer fake_token"}
        )
        self.assertEqual(response.status_code, 200)

    @patch('src.routes.api.admin.investigadores.investigador_service')
    def test_obtener_investigador_not_found(self, mock_service):
        mock_service.obtener_por_id.side_effect = NotFoundError("No encontrado")
        response = self.client.get(
            "/api/admin/investigadores/invalid",
            headers={"Authorization": "Bearer fake_token"}
        )
        self.assertEqual(response.status_code, 404)

    @patch('src.routes.api.admin.investigadores.investigador_service')
    def test_eliminar_investigador(self, mock_service):
        mock_service.eliminar.return_value = None
        response = self.client.delete(
            "/api/admin/investigadores/123",
            headers={"Authorization": "Bearer fake_token"}
        )
        self.assertEqual(response.status_code, 200)

    @patch('src.routes.api.auth.login.config')
    @patch('src.routes.api.auth.login.pwd_context')
    def test_login_success(self, mock_pwd, mock_config):
        mock_config.ADMIN_USERNAME = "admin"
        mock_config.ADMIN_PASSWORD_HASH = "hashed_password"
        mock_config.SECRET_KEY = "test-secret-key"
        mock_pwd.verify.return_value = True
        
        response = self.client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    @patch('src.routes.api.auth.login.config')
    @patch('src.routes.api.auth.login.pwd_context')
    def test_login_invalid_credentials(self, mock_pwd, mock_config):
        mock_config.ADMIN_USERNAME = "admin"
        mock_config.ADMIN_PASSWORD_HASH = "hashed_password"
        mock_pwd.verify.return_value = False
        
        response = self.client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "wrong"}
        )
        self.assertEqual(response.status_code, 401)

    @patch('src.routes.api.public.institucion.institucion_service')
    def test_obtener_configuracion_publica(self, mock_service):
        mock_service.obtener_configuracion.return_value = {
            "nombre": "Test University",
            "logo_principal_url": "https://example.com/logo.png"
        }
        response = self.client.get("/api/public/institucion")
        self.assertEqual(response.status_code, 200)
        self.assertIn("nombre", response.json())

    @patch('src.routes.api.datos.authors.load_json_file')
    def test_get_autores(self, mock_load):
        mock_load.return_value = [{"nombre": "Test Author"}]
        response = self.client.get("/api/datos/authors")
        self.assertEqual(response.status_code, 200)
        self.assertIn("autores", response.json())

    @patch('src.routes.api.datos.documents.load_json_file')
    def test_get_documentos(self, mock_load):
        mock_load.return_value = {"doc1": []}
        response = self.client.get("/api/datos/documents")
        self.assertEqual(response.status_code, 200)
        self.assertIn("documentos", response.json())

if __name__ == '__main__':
    unittest.main()
