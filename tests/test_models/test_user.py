"""Tests pour les modèles."""
import pytest
from demo_app.models.user import User


def test_user_creation():
    """Test de création d'utilisateur."""
    user = User(1, "Test User", "test@example.com")

    assert user.id == 1
    assert user.name == "Test User"
    assert user.email == "test@example.com"
    assert user.active is True


def test_user_to_dict():
    """Test de conversion en dictionnaire."""
    user = User(1, "Test User", "test@example.com", False)
    user_dict = user.to_dict()

    expected = {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
        "active": False,
    }

    assert user_dict == expected


def test_user_from_dict():
    """Test de création depuis un dictionnaire."""
    data = {"id": 2, "name": "Jane Doe", "email": "jane@example.com", "active": True}

    user = User.from_dict(data)

    assert user.id == 2
    assert user.name == "Jane Doe"
    assert user.email == "jane@example.com"
    assert user.active is True
