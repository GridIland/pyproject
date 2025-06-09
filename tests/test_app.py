"""Tests pour l'application principale."""
import pytest
from demo_app.app import create_app


@pytest.fixture
def client():
    """Client de test Flask."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_hello(client):
    """Test de la route principale."""
    response = client.get("/")
    """Tests pour l'application principale."""

    @pytest.fixture
    def client():
        """Client de test Flask."""
        app = create_app()
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_hello(client):
        """Test de la route principale."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Hello World!"
        assert data["status"] == "success"
        assert data["app"] == "demo-app"

    def test_health(client):
        """Test de la route de santé."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"

    def test_info(client):
        """Test de la route d'informations."""
        response = client.get("/api/info")
        assert response.status_code == 200
        data = response.get_json()
        assert "name" in data
        assert "version" in data
        assert data["name"] == "demo-app"

    # Additional tests
    def test_info_version_format(client):
        """Test du format de la version."""
        response = client.get("/api/info")
        data = response.get_json()
        assert "version" in data
        # Check version format (x.y.z)
        version_parts = data["version"].split(".")
        assert len(version_parts) == 3
        assert all(part.isdigit() for part in version_parts)

    def test_invalid_route(client):
        """Test d'une route invalide."""
        response = client.get("/invalid")
        assert response.status_code == 404

    def test_method_not_allowed(client):
        """Test méthode non autorisée."""
        response = client.post("/")
        assert response.status_code == 405

    def test_content_type(client):
        """Test du content-type de la réponse."""
        response = client.get("/")
        assert response.content_type == "application/json"

    # To run tests:
    # 1. Open terminal in project root
    # 2. Run: pytest
    # 3. For coverage: pytest --cov=demo_app
    # 4. For verbose output: pytest -v
    # 5. For specific test: pytest tests/test_app.py::test_hello
