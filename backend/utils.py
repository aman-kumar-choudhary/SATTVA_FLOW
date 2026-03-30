import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from config import Config

# ── Firebase Admin SDK setup ──────────────────────────────────────────────────
# Install: pip install firebase-admin
# Set env var FIREBASE_SERVICE_ACCOUNT_KEY to the path of your service account JSON
# OR set GOOGLE_APPLICATION_CREDENTIALS (same thing)

import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
import os

def _init_firebase():
    """Initialize Firebase Admin SDK (idempotent)."""
    if not firebase_admin._apps:
        key_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')
        if key_path and os.path.exists(key_path):
            cred = credentials.Certificate(key_path)
        else:
            # Falls back to GOOGLE_APPLICATION_CREDENTIALS env var automatically
            cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)

_init_firebase()


def verify_google_token(id_token):
    """
    Verify a Firebase ID token and return the user's info dict, or None on failure.
    The frontend gets this token via: await firebaseUser.getIdToken()
    """
    try:
        decoded = firebase_auth.verify_id_token(id_token)

        email = decoded.get('email', '')
        if not decoded.get('email_verified', False):
            print(f"Firebase token: email not verified for {email}")
            return None

        return {
            'google_id': decoded['uid'],       # Firebase UID == Google sub
            'email':     email,
            'name':      decoded.get('name', ''),
            'picture':   decoded.get('picture', ''),
        }
    except firebase_auth.ExpiredIdTokenError:
        print("Firebase token: expired")
        return None
    except firebase_auth.InvalidIdTokenError as e:
        print(f"Firebase token: invalid — {e}")
        return None
    except Exception as e:
        print(f"Firebase token verification error: {e}")
        return None


# ── Notifications (unchanged) ─────────────────────────────────────────────────

def send_notification(user, title, message, notification_type='info'):
    """Send notification via WhatsApp and Email based on user preferences"""
    whatsapp_sent = False
    email_sent = False

    if user.get('phone') and user.get('settings', {}).get('whatsapp_notifications', True):
        try:
            client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=f"SattvaFlow: {title}\n\n{message}",
                from_=f'whatsapp:{Config.TWILIO_WHATSAPP_NUMBER}',
                to=f'whatsapp:{user["phone"]}'
            )
            whatsapp_sent = True
        except Exception:
            pass

    if user.get('email') and user.get('settings', {}).get('email_notifications', True):
        try:
            msg = MIMEMultipart()
            msg['From'] = Config.EMAIL_USER
            msg['To'] = user['email']
            msg['Subject'] = f"SattvaFlow: {title}"

            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5dc; padding: 20px;">
                <div style="max-width: 500px; margin: 0 auto; background: white; border-radius: 12px; padding: 30px;">
                    <h2 style="color: #7C9A6D;">SattvaFlow</h2>
                    <h3>{title}</h3>
                    <p>{message}</p>
                    <hr style="margin: 20px 0;">
                    <p style="color: #aaa; font-size: 12px;">Find Your Flow with SattvaFlow</p>
                </div>
            </body>
            </html>
            """

            msg.attach(MIMEText(body, 'html'))

            server = smtplib.SMTP(Config.EMAIL_HOST, Config.EMAIL_PORT)
            server.starttls()
            server.login(Config.EMAIL_USER, Config.EMAIL_PASS)
            server.send_message(msg)
            server.quit()
            email_sent = True
        except Exception:
            pass

    return whatsapp_sent or email_sent


# ── Validators ────────────────────────────────────────────────────────────────

def validate_phone(phone):
    """Validate phone number format (basic validation)"""
    import re
    pattern = r'^\+?[1-9]\d{1,14}$'
    return re.match(pattern, phone) is not None


def validate_email(email):
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None