"""Modèle utilisateur d'exemple."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Modèle utilisateur simple."""

    id: int
    name: str
    email: str
    active: bool = True

    def to_dict(self):
        """Convertit en dictionnaire."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "active": self.active,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Crée un utilisateur depuis un dictionnaire."""
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            age=data["age"],
            active=data.get("active", True),
        )
