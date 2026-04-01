# utils.py
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from config import Config
import os
import logging

logger = logging.getLogger(__name__)

def init_firebase():
    """Initialize Firebase Admin SDK"""
    if firebase_admin._apps:
        return
    
    key_path = Config.FIREBASE_SERVICE_ACCOUNT_KEY
    if key_path and os.path.exists(key_path):
        cred = credentials.Certificate(key_path)
    else:
        # Try environment variable
        cred = credentials.ApplicationDefault()
    
    firebase_admin.initialize_app(cred)
    logger.info("Firebase initialized")

def verify_google_token(id_token):
    """Verify Firebase ID token"""
    try:
        init_firebase()
        decoded = firebase_auth.verify_id_token(id_token)
        
        email = decoded.get('email', '')
        if not decoded.get('email_verified', False):
            logger.warning(f"Email not verified: {email}")
            return None
        
        return {
            'google_id': decoded['uid'],
            'email': email,
            'name': decoded.get('name', ''),
            'picture': decoded.get('picture', '')
        }
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        return None

def validate_email(email):
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """Validate phone number"""
    import re
    pattern = r'^\+?[1-9]\d{1,14}$'
    return bool(re.match(pattern, phone or ''))