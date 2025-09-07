import re


class UserUtils:
    @staticmethod
    def password_strength(password: str) -> bool:
        """Check if the password meets strength requirements."""
        if (len(password) < 8 or
            not re.search(r"[A-Z]", password) or
            not re.search(r"[a-z]", password) or
            not re.search(r"[0-9]", password) or
            not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
            return False
        return True
    
    @staticmethod
    def passwords_match(password: str, confirm_password: str) -> bool:
        """Check if the password and confirm password match."""
        return password == confirm_password
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate the email format."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None
    
    @staticmethod
    def validate_phone_number(phone_number: str) -> bool:
        """Validate the phone number format (simple check)."""
        phone_regex = r'^\+?1?\d{9,15}$'
        return re.match(phone_regex, phone_number) is not None
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Sanitize input to prevent XSS attacks."""
        sanitized = re.sub(r'[<>"]', '', input_str)
        return sanitized.strip()
    
    @staticmethod
    def generate_username(email: str) -> str:
        """Generate a username from the email."""
        username = email.split('@')[0]
        username = re.sub(r'[^a-zA-Z0-9]', '', username)
        return username[:30]
    
    @staticmethod
    def is_username_available(username: str, user_model) -> bool:
        """Check if the username is available in the database."""
        return not user_model.objects.filter(username=username).exists()
    
    @staticmethod
    def is_email_available(email: str, user_model) -> bool:
        """Check if the email is available in the database."""
        return not user_model.objects.filter(email=email).exists()
    

    