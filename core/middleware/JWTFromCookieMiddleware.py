# core/middleware/JWTFromCookieMiddleware.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.utils import Utils

class JWTFromCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.utils = Utils()

    def __call__(self, request):
        if not hasattr(request, 'user') or request.user.is_anonymous:
            user = self.utils.get_authenticated_user(request)
            if user:
                request.user = user
        return self.get_response(request)