from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta
from config import Config

def generate_jwt(user_id, role):
    """Generate JWT token for authenticated user"""
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES,
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt(token):
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            payload = decode_jwt(token)
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            request.user = payload
        except Exception as e:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated

def role_required(roles):
    """Decorator to check user role"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_role = request.user.get('role')
            if user_role not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

def admin_required(f):
    """Decorator for admin-only routes"""
    return role_required(['admin'])(f)

def trainer_required(f):
    """Decorator for trainer-only routes"""
    return role_required(['trainer', 'admin'])(f)

def client_required(f):
    """Decorator for client-only routes"""
    return role_required(['client', 'admin'])(f)