# notification_service.py - Complete updated version with all email templates
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """Centralized notification service for email and WhatsApp"""

    # ── EMAIL TEMPLATES ──────────────────────────────────────────────────

    @staticmethod
    def _base_layout(content: str, title: str = 'SattvaFlow') -> str:
        """Wrap content in a consistent branded email layout."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <style>
            body {{ margin: 0; padding: 0; background: #f4f4f0; font-family: 'Georgia', serif; color: #1a1a18; }}
            .wrapper {{ max-width: 600px; margin: 32px auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.08); }}
            .header {{ background: #1a1a18; padding: 28px 36px; display: flex; align-items: center; gap: 12px; }}
            .header-logo {{ font-size: 28px; }}
            .header-brand {{ font-size: 22px; color: #ffffff; letter-spacing: 0.5px; }}
            .body {{ padding: 36px; }}
            .body h2 {{ font-size: 22px; color: #1a1a18; margin: 0 0 16px 0; }}
            .body p {{ font-size: 15px; line-height: 1.7; color: #4a4a46; margin: 0 0 14px 0; }}
            .body ul {{ padding-left: 20px; color: #4a4a46; font-size: 15px; line-height: 1.8; }}
            .detail-box {{ background: #f8f9f4; border-left: 4px solid #4a7c59; border-radius: 6px; padding: 16px 20px; margin: 20px 0; }}
            .detail-box p {{ margin: 4px 0; font-size: 14px; }}
            .detail-box strong {{ color: #1a1a18; }}
            .progress-bar-outer {{ background: #e8e8e2; border-radius: 8px; height: 12px; margin: 10px 0; overflow: hidden; }}
            .progress-bar-inner {{ background: #4a7c59; height: 100%; border-radius: 8px; }}
            .cta-btn {{ display: inline-block; background: #4a7c59; color: #ffffff; padding: 12px 28px; border-radius: 6px; text-decoration: none; font-size: 15px; margin: 20px 0; font-family: sans-serif; }}
            .footer {{ background: #f8f9f4; padding: 20px 36px; border-top: 1px solid #e8e8e2; }}
            .footer p {{ font-size: 12px; color: #9a9a96; margin: 0; }}
            .namaste {{ font-size: 15px; color: #4a4a46; margin-top: 24px; padding-top: 20px; border-top: 1px solid #e8e8e2; }}
          </style>
        </head>
        <body>
          <div class="wrapper">
            <div class="header">
              <div class="header-logo">🌿</div>
              <div class="header-brand">SattvaFlow</div>
            </div>
            <div class="body">
              {content}
              <div class="namaste">
                <p>Namaste,<br><strong>The SattvaFlow Team</strong></p>
              </div>
            </div>
            <div class="footer">
              <p>You received this email because you are registered on SattvaFlow. If you have questions, contact your admin.</p>
            </div>
          </div>
        </body>
        </html>
        """

    @classmethod
    def welcome_client(cls, name: str) -> str:
        content = f"""
        <h2>Welcome to SattvaFlow, {name}! 🙏</h2>
        <p>Your account has been created. Once admin activates your account, you'll be able to:</p>
        <ul>
          <li>View your assigned trainer</li>
          <li>Access personalized yoga plans</li>
          <li>Track your session progress</li>
          <li>Receive session reminders</li>
        </ul>
        <p>We'll notify you as soon as your account is activated.</p>
        """
        return cls._base_layout(content)

    @classmethod
    def welcome_trainer(cls, name: str) -> str:
        content = f"""
        <h2>Welcome to SattvaFlow, {name}! 🧘</h2>
        <p>Your trainer application has been submitted. Admin will review your credentials and approve your account.</p>
        <p>Once approved, you'll be able to manage clients, create yoga plans, and schedule sessions.</p>
        <p>You'll receive a notification when your account is approved.</p>
        """
        return cls._base_layout(content)

    @classmethod
    def account_activated(cls, name: str, dashboard_url: str = '#') -> str:
        content = f"""
        <h2>Account Activated! 🎉</h2>
        <p>Hi {name}, your SattvaFlow account has been <strong>activated by admin</strong>.</p>
        <p>You can now log in and access all your features, including your yoga plan and session schedule.</p>
        <a href="{dashboard_url}" class="cta-btn">Go to Dashboard</a>
        """
        return cls._base_layout(content)

    @classmethod
    def trainer_approved(cls, name: str, dashboard_url: str = '#') -> str:
        content = f"""
        <h2>Congratulations, {name}! 🎊</h2>
        <p>Your trainer application has been <strong>approved</strong> by admin.</p>
        <p>You can now log in to your trainer dashboard, view assigned clients, create yoga plans, and schedule sessions.</p>
        <a href="{dashboard_url}" class="cta-btn">Open Trainer Dashboard</a>
        """
        return cls._base_layout(content)

    @classmethod
    def trainer_rejected(cls, name: str, reason: str) -> str:
        content = f"""
        <h2>Application Update</h2>
        <p>Hi {name}, unfortunately your trainer application was <strong>not approved</strong> at this time.</p>
        <div class="detail-box">
          <p><strong>Reason:</strong> {reason}</p>
        </div>
        <p>Please contact the admin if you have questions or would like to reapply.</p>
        """
        return cls._base_layout(content)

    @classmethod
    def account_blocked(cls, name: str, role: str) -> str:
        content = f"""
        <h2>Account Blocked</h2>
        <p>Hi {name}, your SattvaFlow {role} account has been <strong>blocked by admin</strong>.</p>
        <p>Please contact the admin for more information or to resolve the issue.</p>
        """
        return cls._base_layout(content)

    @classmethod
    def account_unblocked(cls, name: str) -> str:
        content = f"""
        <h2>Account Unblocked ✅</h2>
        <p>Hi {name}, your SattvaFlow account has been <strong>unblocked</strong>. You can now log in again.</p>
        """
        return cls._base_layout(content)

    @classmethod
    def trainer_assigned(cls, client_name: str, trainer_name: str, specialization: str, experience: int) -> str:
        content = f"""
        <h2>Trainer Assigned! 🧘</h2>
        <p>Hi {client_name}, you have been assigned a trainer:</p>
        <div class="detail-box">
          <p><strong>Trainer:</strong> {trainer_name}</p>
          <p><strong>Specialization:</strong> {specialization}</p>
          <p><strong>Experience:</strong> {experience} years</p>
        </div>
        <p>Your trainer will create a personalized yoga plan for you shortly.</p>
        """
        return cls._base_layout(content)

    @classmethod
    def new_client_assigned(cls, trainer_name: str, client_name: str, dashboard_url: str = '#') -> str:
        content = f"""
        <h2>New Client Assigned 👤</h2>
        <p>Hi {trainer_name}, a new client has been assigned to you:</p>
        <div class="detail-box">
          <p><strong>Client:</strong> {client_name}</p>
        </div>
        <p>Please create a personalized yoga plan for them and schedule their first session.</p>
        <a href="{dashboard_url}" class="cta-btn">View Client</a>
        """
        return cls._base_layout(content)

    @classmethod
    def package_assigned(cls, client_name: str, package_title: str, total_sessions: int, total_weeks: int, sessions_per_week: int) -> str:
        content = f"""
        <h2>Package Enrolled: {package_title} 📦</h2>
        <p>Hi {client_name}, you have been enrolled in the following package:</p>
        <div class="detail-box">
          <p><strong>Package:</strong> {package_title}</p>
          <p><strong>Total Sessions:</strong> {total_sessions}</p>
          <p><strong>Duration:</strong> {total_weeks} weeks</p>
          <p><strong>Sessions per week:</strong> {sessions_per_week}</p>
        </div>
        <p>Your trainer will start scheduling sessions for you soon. Track your progress in your dashboard.</p>
        """
        return cls._base_layout(content)

    @classmethod
    def session_scheduled(cls, recipient_name: str, session_title: str, date_str: str, duration: int, client_name: str = None, trainer_name: str = None) -> str:
        details = f"<p><strong>Title:</strong> {session_title}</p><p><strong>Date &amp; Time:</strong> {date_str}</p><p><strong>Duration:</strong> {duration} minutes</p>"
        if client_name:
            details += f"<p><strong>Client:</strong> {client_name}</p>"
        if trainer_name:
            details += f"<p><strong>Trainer:</strong> {trainer_name}</p>"
        content = f"""
        <h2>Session Scheduled: {session_title} 📅</h2>
        <p>Hi {recipient_name}, a session has been scheduled for you:</p>
        <div class="detail-box">{details}</div>
        <p>Please mark your calendar. Your trainer will be in touch.</p>
        """
        return cls._base_layout(content)

    @classmethod
    def session_updated(cls, recipient_name: str, session_title: str) -> str:
        content = f"""
        <h2>Session Updated ✏️</h2>
        <p>Hi {recipient_name}, your session <strong>{session_title}</strong> has been updated by admin.</p>
        <p>Please check your dashboard for the latest details.</p>
        """
        return cls._base_layout(content)

    @classmethod
    def attendance_marked(cls, client_name: str, session_title: str, completed: int, total: int, pending: int) -> str:
        pct = int((completed / total) * 100) if total else 0
        content = f"""
        <h2>Session Completed ✅</h2>
        <p>Hi {client_name}, your session <strong>{session_title}</strong> has been marked as attended.</p>
        <div class="detail-box">
          <p><strong>Classes Completed:</strong> {completed}</p>
          <p><strong>Classes Remaining:</strong> {pending}</p>
          <p><strong>Total Classes:</strong> {total}</p>
        </div>
        <p><strong>Your Progress:</strong> {pct}%</p>
        <div class="progress-bar-outer">
          <div class="progress-bar-inner" style="width:{pct}%"></div>
        </div>
        <p>Keep it up! {'🎉 You have completed your package!' if pending == 0 else f'{pending} more sessions to go.'}</p>
        """
        return cls._base_layout(content)

    @classmethod
    def query_response(cls, client_name: str, query_subject: str, response_text: str) -> str:
        content = f"""
        <h2>Response to Your Query 💬</h2>
        <p>Hi {client_name}, admin has responded to your query:</p>
        <div class="detail-box">
          <p><strong>Your Query:</strong> {query_subject}</p>
        </div>
        <div class="detail-box" style="border-left-color:#2980b9;">
          <p><strong>Admin Response:</strong></p>
          <p>{response_text}</p>
        </div>
        <p>If you have further questions, please submit a new query from your dashboard.</p>
        """
        return cls._base_layout(content)

    @classmethod
    def new_registration_admin(cls, role: str, name: str, email: str, phone: str, admin_url: str = '#') -> str:
        content = f"""
        <h2>New {role.title()} Registration 🔔</h2>
        <p>A new {role} has registered and requires your attention:</p>
        <div class="detail-box">
          <p><strong>Name:</strong> {name}</p>
          <p><strong>Email:</strong> {email or '—'}</p>
          <p><strong>Phone:</strong> {phone or '—'}</p>
          <p><strong>Role:</strong> {role.title()}</p>
        </div>
        <a href="{admin_url}" class="cta-btn">Review in Dashboard</a>
        """
        return cls._base_layout(content)

    # ── SEND METHODS ────────────────────────────────────────────────────

    @classmethod
    def send_email(cls, to_email: str, subject: str, html_content: str) -> bool:
        """Send a single email."""
        if not Config.EMAIL_USER or not Config.EMAIL_PASS:
            logger.warning("Email credentials not configured — skipping email")
            return False
        if not to_email:
            return False

        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = f"SattvaFlow <{getattr(Config, 'EMAIL_FROM', Config.EMAIL_USER)}>"
            msg['To'] = to_email
            msg['Subject'] = subject

            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            with smtplib.SMTP(Config.EMAIL_HOST, Config.EMAIL_PORT, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.login(Config.EMAIL_USER, Config.EMAIL_PASS)
                server.send_message(msg)

            logger.info(f"✅ Email sent → {to_email} | {subject}")
            return True
        except Exception as e:
            logger.error(f"❌ Email failed → {to_email}: {e}")
            return False

    @classmethod
    def send_whatsapp(cls, to_phone: str, message: str) -> bool:
        """Send WhatsApp message via Twilio."""
        if not getattr(Config, 'TWILIO_ACCOUNT_SID', None) or not getattr(Config, 'TWILIO_WHATSAPP_NUMBER', None):
            logger.warning("Twilio not configured — skipping WhatsApp")
            return False
        if not to_phone:
            return False

        try:
            from twilio.rest import Client as TwilioClient
            client = TwilioClient(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=f"SattvaFlow: {message}",
                from_=f'whatsapp:{Config.TWILIO_WHATSAPP_NUMBER}',
                to=f'whatsapp:{to_phone}'
            )
            logger.info(f"✅ WhatsApp sent → {to_phone}")
            return True
        except Exception as e:
            logger.error(f"❌ WhatsApp failed → {to_phone}: {e}")
            return False

    @classmethod
    def send_notification(cls, user: dict, title: str, message: str, ntype: str = 'info', link=None) -> bool:
        """
        Generic notification dispatcher.
        Sends email and/or WhatsApp based on user preferences.
        For structured emails, prefer calling the typed methods (e.g. send_welcome_client)
        directly from the route and passing the rendered HTML here.
        """
        if not user:
            return False

        preferences = user.get('preferences', {})
        sent = False

        # Email
        if preferences.get('email_notifications', True) and user.get('email'):
            html = cls._base_layout(f"<h2>{title}</h2><p>{message}</p>")
            if cls.send_email(user['email'], f"SattvaFlow: {title}", html):
                sent = True

        # WhatsApp
        if preferences.get('whatsapp_notifications', True) and user.get('phone'):
            short = f"{title}\n\n{message[:200]}"
            if cls.send_whatsapp(user['phone'], short):
                sent = True

        return sent

    # ── CONVENIENCE TYPED DISPATCHERS ─────────────────────────────────

    @classmethod
    def notify_welcome_client(cls, user: dict):
        if user.get('email'):
            cls.send_email(user['email'], "Welcome to SattvaFlow 🌿", cls.welcome_client(user['name']))
        if user.get('phone'):
            cls.send_whatsapp(user['phone'], f"Welcome {user['name']}! Your account has been created. Admin will activate it soon.")

    @classmethod
    def notify_welcome_trainer(cls, user: dict):
        if user.get('email'):
            cls.send_email(user['email'], "Trainer Application Received — SattvaFlow", cls.welcome_trainer(user['name']))
        if user.get('phone'):
            cls.send_whatsapp(user['phone'], f"Hi {user['name']}, your trainer application has been submitted.")

    @classmethod
    def notify_account_activated(cls, user: dict):
        if user.get('email'):
            cls.send_email(user['email'], "Account Activated — SattvaFlow ✅", cls.account_activated(user['name']))
        if user.get('phone'):
            cls.send_whatsapp(user['phone'], f"Hi {user['name']}, your account has been activated! Log in now.")

    @classmethod
    def notify_trainer_approved(cls, user: dict):
        if user.get('email'):
            cls.send_email(user['email'], "Trainer Application Approved 🎊", cls.trainer_approved(user['name']))
        if user.get('phone'):
            cls.send_whatsapp(user['phone'], f"Hi {user['name']}, your trainer application has been approved!")

    @classmethod
    def notify_trainer_rejected(cls, user: dict, reason: str):
        if user.get('email'):
            cls.send_email(user['email'], "Trainer Application Update", cls.trainer_rejected(user['name'], reason))

    @classmethod
    def notify_account_blocked(cls, user: dict, role: str = 'user'):
        if user.get('email'):
            cls.send_email(user['email'], "Account Blocked — SattvaFlow", cls.account_blocked(user['name'], role))

    @classmethod
    def notify_account_unblocked(cls, user: dict):
        if user.get('email'):
            cls.send_email(user['email'], "Account Unblocked ✅ — SattvaFlow", cls.account_unblocked(user['name']))

    @classmethod
    def notify_trainer_assigned(cls, client: dict, trainer: dict):
        if client.get('email'):
            html = cls.trainer_assigned(client['name'], trainer['name'], trainer.get('specialization', ''), trainer.get('experience_years', 0))
            cls.send_email(client['email'], f"Trainer Assigned: {trainer['name']}", html)
        if client.get('phone'):
            cls.send_whatsapp(client['phone'], f"Hi {client['name']}, {trainer['name']} has been assigned as your trainer.")

    @classmethod
    def notify_new_client_to_trainer(cls, trainer: dict, client: dict):
        if trainer.get('email'):
            html = cls.new_client_assigned(trainer['name'], client['name'])
            cls.send_email(trainer['email'], f"New Client Assigned: {client['name']}", html)
        if trainer.get('phone'):
            cls.send_whatsapp(trainer['phone'], f"Hi {trainer['name']}, new client {client['name']} has been assigned to you.")

    @classmethod
    def notify_package_assigned(cls, client: dict, package: dict):
        if client.get('email'):
            spw = max(1, round(package.get('sessions_count', 0) / package.get('duration_weeks', 1)))
            html = cls.package_assigned(client['name'], package['title'], package.get('sessions_count', 0), package.get('duration_weeks', 0), spw)
            cls.send_email(client['email'], f"Package Enrolled: {package['title']}", html)
        if client.get('phone'):
            cls.send_whatsapp(client['phone'], f"You've been enrolled in '{package['title']}' — {package.get('sessions_count')} sessions over {package.get('duration_weeks')} weeks.")

    @classmethod
    def notify_session_scheduled(cls, client: dict, trainer: dict, session: dict):
        from datetime import datetime
        try:
            dt = datetime.fromisoformat(str(session.get('scheduled_at', '')).replace('Z', '+00:00'))
            date_str = dt.strftime('%d %b %Y, %I:%M %p')
        except Exception:
            date_str = str(session.get('scheduled_at', ''))

        dur = session.get('duration_minutes', 60)
        title = session.get('title', 'Session')

        if client.get('email'):
            html = cls.session_scheduled(client['name'], title, date_str, dur, trainer_name=trainer.get('name', ''))
            cls.send_email(client['email'], f"Session Scheduled: {title}", html)
        if client.get('phone'):
            cls.send_whatsapp(client['phone'], f"Session '{title}' scheduled on {date_str} ({dur} min).")

        if trainer.get('email'):
            html = cls.session_scheduled(trainer['name'], title, date_str, dur, client_name=client.get('name', ''))
            cls.send_email(trainer['email'], f"Session Scheduled with {client.get('name', '')}: {title}", html)
        if trainer.get('phone'):
            cls.send_whatsapp(trainer['phone'], f"Session '{title}' with {client.get('name', '')} on {date_str}.")

    @classmethod
    def notify_attendance_marked(cls, client: dict, session: dict, subscription: dict):
        if not client.get('email') and not client.get('phone'):
            return
        completed = subscription.get('completed_sessions', 0)
        total = subscription.get('total_sessions', 0)
        pending = subscription.get('pending_sessions', 0)
        title = session.get('title', 'Session')

        if client.get('email'):
            html = cls.attendance_marked(client['name'], title, completed, total, pending)
            cls.send_email(client['email'], f"Session Completed: {title}", html)
        if client.get('phone'):
            cls.send_whatsapp(client['phone'], f"'{title}' marked complete. {completed}/{total} sessions done, {pending} remaining.")

    @classmethod
    def notify_query_response(cls, user: dict, query_subject: str, response_text: str):
        if user.get('email'):
            html = cls.query_response(user['name'], query_subject, response_text)
            cls.send_email(user['email'], "Response to Your Query — SattvaFlow", html)
        if user.get('phone'):
            cls.send_whatsapp(user['phone'], f"Admin responded to your query '{query_subject}': {response_text[:100]}")

    @classmethod
    def notify_new_registration_admin(cls, admin: dict, role: str, new_user: dict):
        if admin.get('email'):
            html = cls.new_registration_admin(role, new_user.get('name', ''), new_user.get('email', ''), new_user.get('phone', ''))
            cls.send_email(admin['email'], f"New {role.title()} Registration — Action Required", html)