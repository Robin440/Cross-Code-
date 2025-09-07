import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.template import Template, Context
from pathlib import Path
from typing import List, Optional, Dict
import logging
from utils.symbols import success, error, warning, loading, info
from django.conf import settings

logger = logging.getLogger('email')



print(loading("Initializing EmailService..."))

class EmailService:
    """A simple email service for sending emails via SMTP in Django projects."""
    
    def __init__(self):
        self.smtp_server = settings.EMAIL_HOST
        self.smtp_port = settings.EMAIL_PORT
        self.sender_email = settings.EMAIL_HOST_USER
        self.sender_password = settings.EMAIL_HOST_PASSWORD
        self.use_tls = settings.EMAIL_USE_TLS
        self.base_dir = Path(__file__).resolve().parent  # Points to services/email/

    def send_email(
        self,
        subject: str,
        template_name: str,
        recipients: List[str],
        context: Optional[Dict] = None,
        from_email: Optional[str] = None,
    ) -> bool:
        """
        Send an email using SMTP with a specified template.

        Args:
            subject: Email subject
            template_name: Name of the template file (e.g., 'custom_email.html')
            recipients: List of recipient email addresses
            context: Dictionary of context data for template rendering
            from_email: Sender email (defaults to settings.EMAIL_HOST_USER)

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Load the template file from services/email/
            template_path = self.base_dir / template_name
            with open(template_path, 'r') as file:
                template_content = file.read()

            # Render the template with context
            context = context or {}
            template = Template(template_content)
            body = template.render(Context(context))

            # Create message
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = from_email or self.sender_email
            msg['To'] = ', '.join(recipients)

            # Attach HTML body
            msg.attach(MIMEText(body, 'html'))

            # Connect to SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                
                # Login if credentials are provided
                if self.sender_email and self.sender_password:
                    server.login(self.sender_email, self.sender_password)
                
                # Send email
                server.send_message(msg)
                
            logger.info(f"Email sent successfully to {', '.join(recipients)}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    def send_welcome_email(self, recipient: str, username: str,otp:int,token:str) -> bool:
        """Send a welcome email to a new user."""
        try:
            subject = "Welcome to Cross Code!"
            link = f"https://{settings.DOMAIN}/verify-email?email={recipient}&otp={otp}&token={token}"
            message = f"Hi {username}, welcome to Cross Code! Please verify your email by clicking the link below."
            additional_info = "If you did not sign up for this account, please ignore this email. and the link will expire in 10 minutes"

            context = {'username': username, 'subject': subject,'otp': otp,"link":link, 'message': message, 'additional_info': additional_info}
            return self.send_email(subject, 'custom_email.html', [recipient], context)
        except Exception as e:
            logger.error(
                        F"Failed to send welcome email to {recipient}: {str(e)}",
                        extra={'service': 'EMAIL SERVICE'},
                        exc_info=True 
                    )
            return False

    def send_password_reset_email(self, recipient: str, reset_link: str) -> bool:
        """Send a password reset email with a reset link."""
        subject = "Password Reset Request"
        context = {'reset_link': reset_link, 'subject': subject}
        return self.send_email(subject, 'password_reset_email.html', [recipient], context)
    

print(success("EmailService initialized successfully."))
print(info("EmailService is ready to send emails."))