# notification_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client as TwilioClient
from config import Config
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """Centralized notification service for email and WhatsApp"""
    
    EMAIL_TEMPLATES = {
        'welcome_client': """
            <h2>Welcome to SattvaFlow, {name}!</h2>
            <p>Your account has been created successfully. Once admin activates your account, you'll be able to:</p>
            <ul>
                <li>View your assigned trainer</li>
                <li>Access personalized yoga plans</li>
                <li>Track your session progress</li>
                <li>Receive session reminders</li>
            </ul>
            <p>We'll notify you as soon as your account is activated.</p>
            <br>
            <p>Namaste,<br>SattvaFlow Team</p>
        """,
        
        'welcome_trainer': """
            <h2>Welcome to SattvaFlow, {name}!</h2>
            <p>Your trainer application has been submitted. Admin will review your credentials and approve your account.</p>
            <p>Once approved, you'll be able to:</p>
            <ul>
                <li>View assigned clients</li>
                <li>Create yoga plans</li>
                <li>Track client progress</li>
                <li>Schedule sessions</li>
            </ul>
            <p>You'll receive a notification when your account is approved.</p>
            <br>
            <p>Namaste,<br>SattvaFlow Team</p>
        """,
        
        'trainer_approved': """
            <h2>Congratulations, {name}!</h2>
            <p>Your trainer application has been approved by admin.</p>
            <p>You can now log in to your trainer dashboard and start working with clients.</p>
            <p><a href="{dashboard_url}">Click here to access your dashboard</a></p>
            <br>
            <p>Namaste,<br>SattvaFlow Team</p>
        """,
        
        'account_activated': """
            <h2>Account Activated, {name}!</h2>
            <p>Your SattvaFlow account has been activated by admin.</p>
            <p>You can now log in and access all features.</p>
            <p><a href="{dashboard_url}">Click here to access your dashboard</a></p>
            <br>
            <p>Namaste,<br>SattvaFlow Team</p>
        """,
        
        'trainer_assigned': """
            <h2>Trainer Assigned!</h2>
            <p>Dear {client_name},</p>
            <p>You have been assigned to trainer <strong>{trainer_name}</strong>.</p>
            <p>{trainer_name} specializes in {specialization} and has {experience} years of experience.</p>
            <p>Your trainer will create personalized yoga plans for you shortly.</p>
            <br>
            <p>Namaste,<br>SattvaFlow Team</p>
        """,
        
        'new_client_assigned': """
            <h2>New Client Assigned!</h2>
            <p>Dear {trainer_name},</p>
            <p>A new client <strong>{client_name}</strong> has been assigned to you.</p>
            <p>Please create a personalized yoga plan for them.</p>
            <p><a href="{dashboard_url}">Click here to view client details</a></p>
            <br>
            <p>Namaste,<br>SattvaFlow Team</p>
        """,
        
        'session_scheduled': """
            <h2>Session Scheduled: {title}</h2>
            <p>Dear {name},</p>
            <p>A new session has been scheduled:</p>
            <ul>
                <li><strong>Title:</strong> {title}</li>
                <li><strong>Date:</strong> {date}</li>
                <li><strong>Time:</strong> {time}</li>
                <li><strong>Duration:</strong> {duration} minutes</li>
            </ul>
            <p>Please mark your calendar.</p>
            <br>
            <p>Namaste,<br>SattvaFlow Team</p>
        """,
        
        'query_response': """
            <h2>Response to Your Query</h2>
            <p>Dear {name},</p>
            <p><strong>Your Query:</strong> {query_subject}</p>
            <p><strong>Admin Response:</strong></p>
            <p>{response}</p>
            <br>
            <p>Namaste,<br>SattvaFlow Team</p>
        """,
        
        'new_message': """
            <h2>New Message from {sender_name}</h2>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Message:</strong></p>
            <p>{message_preview}</p>
            <p><a href="{messages_url}">Click here to view and reply</a></p>
            <br>
            <p>Namaste,<br>SattvaFlow Team</p>
        """,
        
        'review_pending': """
            <h2>New Review Pending Approval</h2>
            <p>A client has submitted a review for trainer {trainer_name}.</p>
            <p>Please review and approve it.</p>
            <p><a href="{admin_url}">Click here to moderate</a></p>
        """,
        
        'registration_notification': """
            <h2>New {role} Registration</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Phone:</strong> {phone}</p>
            <p><strong>Role:</strong> {role}</p>
            <p><a href="{admin_url}">Click here to review</a></p>
        """
    }
    
    @classmethod
    def send_email(cls, to_email, subject, html_content):
        """Send email notification"""
        if not Config.EMAIL_USER or not Config.EMAIL_PASS:
            logger.warning("Email credentials not configured")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = f"SattvaFlow <{Config.EMAIL_FROM}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(Config.EMAIL_HOST, Config.EMAIL_PORT) as server:
                server.ehlo()
                server.starttls()
                server.login(Config.EMAIL_USER, Config.EMAIL_PASS)
                server.send_message(msg)
            
            logger.info(f"Email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    @classmethod
    def send_whatsapp(cls, to_phone, message):
        """Send WhatsApp notification via Twilio"""
        if not Config.TWILIO_ACCOUNT_SID or not Config.TWILIO_WHATSAPP_NUMBER:
            logger.warning("Twilio credentials not configured")
            return False
        
        try:
            client = TwilioClient(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=f"SattvaFlow: {message}",
                from_=f'whatsapp:{Config.TWILIO_WHATSAPP_NUMBER}',
                to=f'whatsapp:{to_phone}'
            )
            logger.info(f"WhatsApp sent to {to_phone}")
            return True
        except Exception as e:
            logger.error(f"Failed to send WhatsApp to {to_phone}: {e}")
            return False
    
    @classmethod
    def send_notification(cls, user, title, message, ntype='info', link=None):
        """Send notification through user's preferred channels"""
        if not user:
            return False
        
        preferences = user.get('preferences', {})
        sent = False
        
        # Send email if enabled
        if preferences.get('email_notifications', True) and user.get('email'):
            html = cls.EMAIL_TEMPLATES.get(ntype, cls._default_html_template(title, message))
            if '{' in html:  # Template needs formatting
                html = cls._format_template(html, user, {'title': title, 'message': message, 'link': link})
            else:
                html = cls._default_html_template(title, message)
            
            if cls.send_email(user['email'], f"SattvaFlow: {title}", html):
                sent = True
        
        # Send WhatsApp if enabled and phone exists
        if preferences.get('whatsapp_notifications', True) and user.get('phone'):
            whatsapp_msg = f"{title}\n\n{message[:200]}"
            if cls.send_whatsapp(user['phone'], whatsapp_msg):
                sent = True
        
        return sent
    
    @classmethod
    def _default_html_template(cls, title, message):
        return f"""
        <h2>{title}</h2>
        <p>{message}</p>
        <br>
        <p>Namaste,<br>SattvaFlow Team</p>
        """
    
    @classmethod
    def _format_template(cls, template, user, context):
        """Format email template with context"""
        try:
            return template.format(**context, **user)
        except KeyError:
            return template