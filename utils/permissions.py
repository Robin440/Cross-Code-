# account/permissions.py
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.response import Response
from django.contrib import messages
from utils.utils import Utils
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.contrib.auth.models import AnonymousUser
import logging
logger = logging.getLogger("PERMISSIONS")
     


class CustomIsAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        logger.debug(f"Checking permission for user: {user}, is_authenticated: {user.is_authenticated}")

        # Check if the user is authenticated
        if isinstance(user, AnonymousUser) or not user.is_authenticated:
            logger.warning(f"Unauthenticated access attempt by {user}")
            return False
        return True