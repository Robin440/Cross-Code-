
import datetime

from rest_framework.permissions import IsAuthenticated
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class Utils:
    def __init__(self):
        self.jwt_auth = JWTAuthentication()


    @staticmethod
    def generate_otp_6_digit() -> str:
        """Generate a random 6-digit OTP."""
        import random
        return f"{random.randint(100000, 999999)}"
    
    @staticmethod
    def generate_token() -> str:
        """Generate a random token."""
        import secrets
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_otp_expiry(minutes: int = 10) -> 'datetime':
        """Generate an expiry datetime for OTP."""
        from datetime import datetime, timedelta
        return datetime.now() + timedelta(minutes=minutes)
    
    @staticmethod
    def current_time() -> 'datetime':
        """Get the current UTC time."""
        from datetime import datetime
        return datetime.utcnow()
    
    @staticmethod
    def generate_otp_8_digit() -> str:
        """Generate a random 8-digit OTP."""
        import random
        return f"{random.randint(10000000, 99999999)}"
    

# utils/utils.py


logger = logging.getLogger("account")

class Utils:
    def __init__(self):
        self.jwt_auth = JWTAuthentication()

    def get_authenticated_user(self, request):
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            else:
                token = request.COOKIES.get('access_token')
                if not token:
                    token_data = request.session.get('token_data', {})
                    token = token_data.get('access')

            if not token:
                logger.debug("No JWT token found in header, cookie, or session", extra={"service": "USER SERVICE"})
                return None

            validated_token = self.jwt_auth.get_validated_token(token)
            user = self.jwt_auth.get_user(validated_token)
            return user

        except AuthenticationFailed as e:
            logger.error(f"JWT authentication failed: {str(e)}", extra={"service": "USER SERVICE"})
            return None
        except Exception as e:
            logger.error(f"Error retrieving authenticated user: {str(e)}", extra={"service": "USER SERVICE"}, exc_info=True)
            return None
    



