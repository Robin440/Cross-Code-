import re
import secrets
import string
import uuid
import random
from datetime import datetime, timedelta, timezone


class UserUtils:
    @staticmethod
    def password_strength(password: str) -> bool:
        """Check if the password meets strength requirements."""
        if (
            len(password) < 8
            or not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"[0-9]", password)
            or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
        ):
            return False
        return True

    @staticmethod
    def passwords_match(password: str, confirm_password: str) -> bool:
        """Check if the password and confirm password match."""
        return password == confirm_password

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate the email format."""
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_regex, email) is not None

    @staticmethod
    def validate_phone_number(phone_number: str) -> bool:
        """Validate the phone number format (simple check)."""
        phone_regex = r"^\+?1?\d{9,15}$"
        return re.match(phone_regex, phone_number) is not None

    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Sanitize input to prevent XSS attacks."""
        sanitized = re.sub(r'[<>"]', "", input_str)
        return sanitized.strip()

    @staticmethod
    def generate_username(email: str) -> str:
        """Generate a username from the email."""
        username = email.split("@")[0]
        username = re.sub(r"[^a-zA-Z0-9]", "", username)
        return username[:30]

    @staticmethod
    def is_username_available(username: str, user_model) -> bool:
        """Check if the username is available in the database."""
        return not user_model.objects.filter(username=username).exists()

    @staticmethod
    def is_email_available(email: str, user_model) -> bool:
        """Check if the email is available in the database."""
        return not user_model.objects.filter(email=email).exists()

    @staticmethod
    def generate_token() -> str:
        """Generate a secure fixed-length 32 character token with randomness + UUID."""
        characters = string.ascii_letters + string.digits

        # 16 random characters
        random_part = "".join(secrets.choice(characters) for _ in range(16))

        # 16 chars from UUID
        uuid_part = uuid.uuid4().hex[:16]

        return f"{random_part}_{uuid_part}[:32]"

    @staticmethod
    def generate_otp(length: int = 6) -> int:
        """
        Generate a numeric OTP of given length.

        :param length: Length of OTP (default is 6).
        :return: OTP as a string.
        """
        return "".join(str(random.randint(0, 9)) for _ in range(length))

    @staticmethod
    def generate_otp_expiry(minutes: int = 5) -> datetime:
        """
        Generate an expiry datetime for OTPs.

        :param minutes: Expiry time in minutes (default = 5).
        :return: A timezone-aware datetime object in UTC.
        """
        return datetime.now(timezone.utc) + timedelta(minutes=minutes)
