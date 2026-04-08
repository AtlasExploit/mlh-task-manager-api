from datetime import datetime, timedelta, timezone
import jwt
from flask import Blueprint, current_app, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from database import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/register')
def register():
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({'error': 'username, email, and password are required'}), 400

    db = get_db()

    existing_user = db.execute(
        'SELECT id FROM users WHERE username = ? OR email = ?',
        (username, email)
    ).fetchone()

    if existing_user:
        return jsonify({'error': 'user with this username or email already exists'}), 409

    password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    db.execute(
        'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
        (username, email, password_hash)
    )
    db.commit()

    return jsonify({'message': 'user registered successfully'}), 201


@auth_bp.post('/login')
def login():
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'email and password are required'}), 400

    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE email = ?',
        (email,)
    ).fetchone()

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'invalid credentials'}), 401

    token = jwt.encode(
        {
            'user_id': user['id'],
            'email': user['email'],
            'exp': datetime.now(timezone.utc) + timedelta(hours=2)
        },
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return jsonify({'token': token, 'username': user['username']})