"""Fonctions utilitaires."""
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """Valide un format d'email."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def sanitize_string(text: str, max_length: int = 100) -> str:
    """Nettoie et limite la longueur d'une chaîne."""
    if not isinstance(text, str):
        return ""

    # Supprime les caractères dangereux
    sanitized = re.sub(r'[<>"\'&]', "", text)

    # Limite la longueur
    return sanitized[:max_length].strip()


def format_response(data, status: str = "success", message: Optional[str] = None):
    """Formate une réponse JSON standard."""
    response = {"status": status, "data": data}

    if message:
        response["message"] = message

    return response
