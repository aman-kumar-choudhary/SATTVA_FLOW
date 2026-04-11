# auth.py
from functools import wraps
from flask import request, jsonify, g
import jwt
from datetime import datetime, timedelta
from config import Config

def generate_jwt(user_id, role):
    """Generate JWT token"""
    payload = {
        'user_id': str(user_id),
        'role': role,
        'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def decode_jwt(token):
    """Decode and verify JWT"""
    try:
        return jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to verify JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header:
            return jsonify({'error': 'Authorization header missing'}), 401

        token = auth_header[7:] if auth_header.startswith('Bearer ') else auth_header

        payload = decode_jwt(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401

        # Store on flask.g — the correct per-request context store in Flask.
        # Also mirror to request.user for any existing code that reads it.
        g.user = payload
        request.user = payload
        return f(*args, **kwargs)
    return decorated

def role_required(*roles):
    """Decorator for role-based access control"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Read from g.user (set by token_required); fall back to request.user
            user_data = getattr(g, 'user', None) or getattr(request, 'user', {})
            user_role = user_data.get('role') if isinstance(user_data, dict) else None
            if user_role not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

def admin_required(f):
    """Admin only decorator"""
    return role_required('admin')(f)

def trainer_required(f):
    """Trainer or admin decorator"""
    return role_required('trainer', 'admin')(f)

def client_required(f):
    """Client or admin decorator"""
    return role_required('client', 'admin')(f)