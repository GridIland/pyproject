# Utilise une image Python officielle
FROM python:3.11-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers de dépendances
COPY requirements.txt .
COPY pyproject.toml .

# Met à jour pip et installe les dépendances
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Copie le code source
COPY . .

# Crée un utilisateur non-root pour la sécurité
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expose le port (ajustez selon votre application)
EXPOSE 5000

# Variables d'environnement
ENV PYTHONPATH=/app
ENV FLASK_APP=demo_app/app.py
ENV FLASK_ENV=production

# Commande par défaut
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]