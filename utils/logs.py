import logging
import os
from django.http import HttpRequest
from threading import local


class RequestContextFilter(logging.Filter):
    def filter(self, record):
        # Use thread-local storage to access request
        request = getattr(local(), 'request', None)
        record.username = getattr(request.user, 'username', 'anonymous') if request and hasattr(request, 'user') else 'anonymous'
        record.request_path = getattr(request, 'path', 'unknown') if request else 'unknown'
        return True