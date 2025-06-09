"""Routes API."""
from flask import Blueprint, jsonify, request
from demo_app.models.user import User

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Données d'exemple en mémoire
users_db = [
    User(1, "Alice Dupont", "alice@example.com"),
    User(2, "Bob Martin", "bob@example.com"),
    User(3, "Charlie Durand", "charlie@example.com", False)
]

@api_bp.route('/users', methods=['GET'])
def get_users():
    """Récupère tous les utilisateurs."""
    active_only = request.args.get('active', 'false').lower() == 'true'
    
    if active_only:
        filtered_users = [u for u in users_db if u.active]
    else:
        filtered_users = users_db
    
    return jsonify({
        'users': [user.to_dict() for user in filtered_users],
        'count': len(filtered_users)
    })

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Récupère un utilisateur par ID."""
    user = next((u for u in users_db if u.id == user_id), None)
    
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    return jsonify(user.to_dict())
