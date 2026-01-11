from flask import Blueprint, request, jsonify
from ..services.auth_service import AuthService # 修正

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Missing username, email or password'}), 400

    try:
        user = AuthService.register_user(username, email, password)
        return jsonify({'message': f'User {user.username} registered successfully'}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 409 # Conflict
    except Exception as e:
        return jsonify({'message': str(e)}), 500 # Internal Server Error

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    try:
        user = AuthService.login_user(username, password)
        if user:
            return jsonify({
                'message': f'User {user.username} logged in successfully',
                'user_id': user.id,
                'username': user.username
            }), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'message': str(e)}), 500

