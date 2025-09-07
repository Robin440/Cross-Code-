

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from account.views.user_views import LoginAPIView

from utils.responses import response_processor


class LandingPageAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'login.html'

    def get(self, request):
        if request.accepted_renderer.format == 'html':
            return Response({})
        return response_processor("Welcome to the API", status.HTTP_200_OK)
    
    def post(self, request):
        """Redirect to LoginAPIView for handling login"""
        login_view = LoginAPIView.as_view()
        return login_view(request._request)