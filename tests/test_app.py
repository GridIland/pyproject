"""Tests pour l'application principale."""
import pytest
from demo_app.app import create_app


@pytest.fixture
def client():
    """Client de test Flask."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_hello(client):
    """Test de la route principale."""
    response = client.get('/')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['message'] == 'Hello World!'
    assert data['status'] == 'success'
    assert data['app'] == 'demo-app'


def test_health(client):
    """Test de la route de santé."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_info(client):
    """Test de la route d'informations."""
    response = client.get('/api/info')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'name' in data
    assert 'version' in data
    assert data['name'] == 'demo-app'
