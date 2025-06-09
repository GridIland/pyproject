"""Tests pour les utilitaires."""
import pytest
from demo_app.utils.helpers import validate_email, sanitize_string, format_response


def test_validate_email():
    """Test de validation d'email."""
    # Emails valides
    assert validate_email("test@example.com") is True
    assert validate_email("user.name+tag@domain.co.uk") is True

    # Emails invalides
    assert validate_email("invalid-email") is False
    assert validate_email("@example.com") is False
    assert validate_email("test@") is False


def test_sanitize_string():
    """Test de nettoyage de chaîne."""
    # Test basique
    assert sanitize_string("Hello World") == "Hello World"

    # Test avec caractères dangereux
    dangerous = "Hello <script>alert('xss')</script>"
    sanitized = sanitize_string(dangerous)
    assert "<script>" not in sanitized
    assert "alert" in sanitized  # Le contenu reste mais les balises sont supprimées

    # Test de limitation de longueur
    long_text = "a" * 200
    short = sanitize_string(long_text, max_length=50)
    assert len(short) == 50


def test_format_response():
    """Test de formatage de réponse."""
    data = {"key": "value"}
    response = format_response(data)

    expected = {"status": "success", "data": {"key": "value"}}

    assert response == expected

    # Avec message
    response_with_msg = format_response(data, "error", "Something went wrong")
    assert response_with_msg["status"] == "error"
    assert response_with_msg["message"] == "Something went wrong"
