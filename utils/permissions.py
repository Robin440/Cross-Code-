# account/permissions.py
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.response import Response
from django.contrib import messages
from utils.utils import Utils
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

class CustomIsAuthenticated(IsAuthenticated):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    
    def has_permission(self, request, view):
        # Initialize Utils to access get_authenticated_user
        utils_manager = Utils()
        # Use get_authenticated_user or request.user (if middleware sets it)
        user = utils_manager.get_authenticated_user(request) or request.user
        print(f"user --------------- {user}")

        # Check if the user is authenticated
        if user and user.is_authenticated:
            print(f"user is_authenticated  {user.is_authenticated}")
            return True

        # Handle unauthenticated user based on renderer
        if request.accepted_renderer.format == "html":
            messages.error(request, "You must be logged in to access this page.")
            return redirect(reverse("login"))
        else:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_403_FORBIDDEN
            )
        

# account/permissions.py
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from django.shortcuts import redirect
# from django.urls import reverse
# from rest_framework.response import Response
# from django.contrib import messages
# from utils.utils import Utils

class CustomIsAuthenticated(IsAuthenticated):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    
    def has_permission(self, request, view):
        # Initialize Utils to access get_authenticated_user
        utils_manager = Utils()
        # Use get_authenticated_user or request.user (if middleware sets it)
        user = utils_manager.get_authenticated_user(request) or request.user
        print(f"user --------------- {user}")

        # Check if the user is authenticated
        if user and user.is_authenticated:
            print(f"user is_authenticated  {user.is_authenticated}")
            return True

        # Handle unauthenticated user based on renderer
        if request.accepted_renderer.format == "html":
            messages.error(request, "You must be logged in to access this page.")
            return redirect(reverse("login"))
        else:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_403_FORBIDDEN
            )