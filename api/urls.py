
from django.contrib import admin
from django.urls import path, include
from core.views import LandingPageAPIView

from account.views.user_views import (
    RegisterAPIView, LoginAPIView, VerifiyOTPAPIView,HomeViewAPIView,
    LogoutAPIView)



urlpatterns = [



    #accounts urls
    path('', LandingPageAPIView.as_view(), name='landing-page'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify-otp/', VerifiyOTPAPIView.as_view(), name='verify-otp'),
    path('home/',HomeViewAPIView.as_view(),name="home"),
    path('logout/', LogoutAPIView.as_view(),name="user_logout")
  ]
