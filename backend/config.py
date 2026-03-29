import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    # MongoDB
    MONGODB_URI = os.getenv('DB_URL', 'mongodb://localhost:27017/sattvaflow')

    # JWT
    JWT_SECRET_KEY          = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES  = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Google OAuth
    GOOGLE_CLIENT_ID     = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')   # ← NEW: required for code exchange

    # Admin
    ADMIN_EMAIL    = os.getenv('ADMIN_EMAIL')
    ADMIN_WHATSAPP = os.getenv('ADMIN_WHATSAPP')
    ADMIN_PHONE    = os.getenv('ADMIN_PHONE')

    # Email
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASS = os.getenv('EMAIL_PASS')

    # WhatsApp / Twilio
    TWILIO_ACCOUNT_SID      = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN       = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER  = os.getenv('TWILIO_WHATSAPP_NUMBER')

    # Frontend
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')

    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret')