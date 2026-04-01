# config.py
import os
from dotenv import load_dotenv
from datetime import timedelta
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    # MongoDB
    MONGODB_URI = os.getenv('DB_URL', 'mongodb://localhost:27017/')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'sattvaflow')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-super-secret-jwt-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Admin (from env)
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@sattvaflow.com')
    ADMIN_NAME = os.getenv('ADMIN_NAME', 'Super Admin')
    ADMIN_PHONE = os.getenv('ADMIN_PHONE', '')
    
    # Firebase
    FIREBASE_SERVICE_ACCOUNT_KEY = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY', 'firebase-service-account.json')
    
    # Email (SMTP)
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASS = os.getenv('EMAIL_PASS')
    EMAIL_FROM = os.getenv('EMAIL_FROM', EMAIL_USER)
    
    # Twilio WhatsApp
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
    
    # Frontend
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'flask-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    # Pagination
    ITEMS_PER_PAGE = int(os.getenv('ITEMS_PER_PAGE', 20))