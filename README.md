# Demo App

Application de démonstration Python avec pipeline Jenkins.

## 🚀 Installation

```bash
# Cloner le repository
git clone <your-repo-url>
cd demo-app

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python demo_app/app.py
```

## 🧪 Tests

```bash
# Exécuter tous les tests
pytest

# Tests avec couverture
pytest --cov=demo_app

# Tests avec rapport HTML
pytest --cov=demo_app --cov-report=html
```

## 🔧 Qualité de code

```bash
# Formater le code
black .

# Trier les imports
isort .

# Linting
flake8 .

# Vérification des types
mypy .
```

## 🐳 Docker

```bash
# Construire l'image
docker build -t demo-app .

# Lancer le conteneur
docker run -p 5000:5000 demo-app
```

## 📊 API Endpoints

- `GET /` - Message de bienvenue
- `GET /health` - Statut de santé
- `GET /api/info` - Informations sur l'application
- `GET /api/users` - Liste des utilisateurs
- `GET /api/users/<id>` - Utilisateur par ID

## 🔄 Pipeline Jenkins

Le pipeline inclut :
- ✅ Tests unitaires
- ✅ Couverture de code
- ✅ Qualité de code (Black, flake8, isort, mypy)
- ✅ Scan de sécurité (Safety, Bandit)
- ✅ Build Docker
- ✅ Déploiement staging/production

## 📝 Structure

```
demo-app/
├── demo_app/          # Code source
├── tests/             # Tests unitaires
├── requirements.txt   # Dépendances
├── pyproject.toml    # Configuration
├── Dockerfile        # Image Docker
└── Jenkinsfile       # Pipeline CI/CD
```
