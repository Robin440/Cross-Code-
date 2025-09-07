
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib import messages
# account/views/user_views.py

# Standard library imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages



# Local imports
from django.contrib.auth import authenticate
from utils.responses import response_processor
from account.utils import UserUtils
from utils.utils import Utils
from services.email.email_service import EmailService
from utils.responses import ResponseService
from django.shortcuts import redirect
from django.urls import reverse
import datetime

import logging

# Models and Serializers
from account.models import CustomUser


logger = logging.getLogger("account")
# logger = logging.getLogger(__name__)


class UserService:
    """Service class for user-related operations."""
    @staticmethod
    def create_user(username, email, password):
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        return user

    @staticmethod
    def get_all_users():
        return CustomUser.objects.all()

    @staticmethod
    def get_user_by_id(user_id):
        return CustomUser.objects.get(id=user_id)
    
    @staticmethod
    def get_user_by_email(email):
        return CustomUser.objects.get(email=email)
    
    @staticmethod
    def get_user_by_uuid(uuid):
        return CustomUser.objects.get(uuid=uuid)    
    

    @staticmethod
    def get_user_by_request(request):
        return request.user
    
    @staticmethod
    def get_user_from_request(request):
        
        if request.user.is_anonymous:
            # Try to authenticate using the token from query parameter or session
            access_token = request.GET.get('access_token') or request.session.get('token_data', {}).get('access')
            if access_token:
                try:
                    # Manually authenticate using JWT
                    jwt_auth = JWTAuthentication()
                    validated_token = jwt_auth.get_validated_token(access_token)
                    user = jwt_auth.get_user(validated_token)
                    print(f"user in tok {user}")
                    # Set the user in the request
                    request.user = user
                    return user
                except Exception as e:
                    logger.error(f"JWT authentication failed: {str(e)}", extra={"service": "USER SERVICE"})
                    if request.accepted_renderer.format == 'html':
                        messages.error(request, "Invalid or expired token.")
                        return redirect(reverse('login'))
                    return Response({"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)
    
