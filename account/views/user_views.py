# account/views/user_views.py

# Standard library imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated
from utils.permissions import CustomIsAuthenticated


# Local imports
from django.contrib.auth import authenticate, logout
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
from account.serializers import UserSerializer, UserCreateSerializer, LoginSerializer
from account.services import UserService
from account.models import Verification

logger = logging.getLogger("account")
# logger = logging.getLogger(__name__)

email_service_manager = EmailService()
user_utils_manager = UserUtils()
utils_manager = Utils()
response_manager = ResponseService()
user_service_manager = UserService()


class LoginAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "login.html"

    def get(self, request):
        if request.accepted_renderer.format == "html":
            return Response({})
        return Response({"message": "Use POST for login"})

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                if request.accepted_renderer.format == "html":
                    return response_manager.HTTP_400(
                        data=f"Invalid input : {str(serializer.errors),}",
                        template_name=self.template_name,
                    )
                return Response(
                    {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, email=email, password=password)
            print(f"user auth : {user}")
            if not user:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            refresh = RefreshToken.for_user(user)
            token_data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            request.session["token_data"] = token_data
            if request.accepted_renderer.format == "html":
                messages.success(request, "Logged in successfully")
                response = redirect(reverse("home"))
                response.set_cookie(
                    "access_token",
                    token_data["access"],
                    httponly=True,
                    secure=False,  # Use secure=True in production (requires HTTPS)
                    samesite="Lax",
                    max_age=3600,  # Match ACCESS_TOKEN_LIFETIME (1 hour)
                )
                messages.success(request, "Logged in successfully")
                return response
            return Response(token_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VerifiyOTPAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "otp.html"

    def get(self, request):
        email = request.GET.get("email") or request.session.get("email")
        if email:
            request.session["email"] = email  # persist for POST
        context = {"email": email}
        if request.accepted_renderer.format == "html":
            return Response(context, template_name=self.template_name)
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        email = (
            request.data.get("email")
            or request.session.get("email")
            or kwargs.get("email")
        )
        print(f"request {request.data}")
        email = request.data.get("email")
        if email:
            request.session["email"] = email
        else:
            email = request.session.get("email")
        try:
            otp = int(request.data.get("otp"))
        except Exception as e:
            return response_manager.HTTP_400(
                data="Invalid OTP!!", template_name=self.template_name
            )
        print(f"type of otp {type(otp)}")
        print(f"email {email} --- otp ; {otp}")
        if not email or not otp:
            if request.accepted_renderer.format == "html":
                return Response(
                    {"error": "Email and OTP are required"},
                    template_name=self.template_name,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"error": "Email and OTP are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = UserService.get_user_by_email(email)
            print(f"user : {user}")
            try:
                verification = Verification.objects.get(
                    user=user, otp=otp, purpose="new_user_verification"
                )
                print(f"veri {verification}")
            except Exception as e:
                print(f"error : {str(e)}")
                logger.error(
                    # message = f"Verification code not found for {user.username} : {user.email} with error {str(e)} ",
                    extra={"service : USER SERVICE"},
                    # service = {"service : USER SERVICE"},
                    msg=f"Verification code not found for {user.username} : {user.email} with error {str(e)} ",
                    exc_info=True,
                )
                return Response(
                    {"error": "Something went wrong."},
                    template_name=self.template_name,
                    status=status.HTTP_404_NOT_FOUND,
                )
            if not verification:
                if request.accepted_renderer.format == "html":
                    return Response(
                        {"error": "Invalid OTP or Email"},
                        template_name=self.template_name,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                return Response(
                    {"error": "Invalid OTP or Email"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # if verification.is_expired():
            #     if request.accepted_renderer.format == "html":
            #         return Response(
            #             {"error": "OTP has expired"},
            #             template_name=self.template_name,
            #             status=status.HTTP_400_BAD_REQUEST,
            #         )
            #     return Response(
            #         {"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST
            # )
            user.verified = True
            user.save()
            verification.delete()  # Remove used OTP
            if request.accepted_renderer.format == "html":
                message = "OTP verified successfully. You can now log in."
                return redirect(reverse("login") + f"?message={message}")
                # return Response(
                #     {
                #         "message": "OTP verified successfully. You can now log in.",
                #         "user": UserSerializer(user).data,
                #     },
                #     template_name="login.html",  # Redirect to login page after successful verification
                # )
            return Response({"message": "OTP verified successfully"})
        except CustomUser.DoesNotExist:
            if request.accepted_renderer.format == "html":
                return Response(
                    {"error": "User does not exist"},
                    template_name=self.template_name,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            if request.accepted_renderer.format == "html":
                return Response(
                    {"error": str(e)},
                    template_name=self.template_name,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RegisterAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "register.html"

    def get(self, request):
        if request.accepted_renderer.format == "html":
            return Response({})
        return Response({"message": "Use POST to register"})

    def post(self, request):
        logger.debug(
            "Processing registration request", extra={"service": "USER SERVICE"}
        )
        serializer = UserCreateSerializer(data=request.data)
        valid_password = user_utils_manager.password_strength(
            request.data.get("password", "")
        )
        if not valid_password:
            logger.warning(
                "Weak password provided during registration",
                extra={"service": "USER SERVICE"},
                exc_info=True,
            )
            if request.accepted_renderer.format == "html":
                return Response(
                    {
                        "error": "Password must be at least 8 characters long and include uppercase, lowercase, digit, and special character."
                    },
                    template_name=self.template_name,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        match_password = request.data.get("password") == request.data.get(
            "confirm_password"
        )
        if not match_password:
            logger.warning(
                "Password and confirm password do not match",
                extra={"service": "USER SERVICE"},
                exc_info=True,
            )
            if request.accepted_renderer.format == "html":
                return Response(
                    {"error": "Password and Confirm Password do not match"},
                    template_name=self.template_name,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                return Response(
                    {"error": "Password and Confirm Password do not match"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        # Proceed if serializer is valid
        if serializer.is_valid():
            try:
                user = serializer.create(serializer.validated_data)
                if not user:
                    logger.error(
                        "User creation failed",
                        extra={"service": "USER SERVICE"},
                        exc_info=True,
                    )
                    return response_processor(
                        success=False,
                        message="User creation failed",
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
                try:
                    verification = Verification.objects.create(
                        user=user,
                        token=utils_manager.generate_token(),
                        otp=utils_manager.generate_otp_6_digit(),
                        purpose="new_user_verification",
                        expires_at=utils_manager.generate_otp_expiry(),
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to create verification record: {str(e)}",
                        extra={"service": "USER SERVICE"},
                        exc_info=True,
                    )
                    return response_processor(
                        success=False,
                        message="Failed to create verification record",
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                # Send welcome email
                # email = email_service_manager.send_welcome_email(
                #     recipient=user.email,
                #     username=user.username,
                #     otp=verification.otp,
                #     token=verification.token
                # )
                #  # Log email sending result
                # if not email:
                #     logger.error(
                #         f"Failed to send welcome email to {user.email}",
                #         extra={'service': 'EMAIL SERVICE'},
                #         exc_info=True
                #     )
                logger.info(
                    f"User {user.username} registered successfully",
                    extra={"service": "USER SERVICE"},
                )
                # Return appropriate response based on request format

                if request.accepted_renderer.format == "html":
                    return redirect(reverse("verify-otp") + f"?email={user.email}")
                else:
                    return response_processor(
                        success=True,
                        message="User registered successfully. Please verify your email.",
                        data=UserSerializer(user).data,
                        status_code=status.HTTP_201_CREATED,
                    )
            except Exception as e:
                logger.error(
                    f"Error during registration: {str(e)}",
                    extra={"service": "USER SERVICE"},
                    exc_info=True,
                )
                if request.accepted_renderer.format == "html":
                    return Response(
                        {
                            "error": f"Registration failed: {str(e)}",
                            "errors": serializer.errors,
                        },
                        template_name=self.template_name,  # Render register.html
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    return Response(
                        {"error": f"Registration failed: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        logger.error(
            f"Invalid input: {serializer.errors}",
            extra={"service": "USER SERVICE"},
            exc_info=True,
        )
        if request.accepted_renderer.format == "html":
            return Response(
                {
                    "error": f"Invalid input : {serializer.errors}",
                    "errors": serializer.errors,
                },
                template_name=self.template_name,
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"error": "Invalid input", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class HomeViewAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "home.html"
    permission_classes = [CustomIsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user  # Use request.user (set by middleware or CustomIsAuthenticated)
        print(f"session {request.session.get('token_data')}")
        print(f"user in home : {user}")
        print(f"Authorization header: {request.META.get('HTTP_AUTHORIZATION')}")
        print(f"Cookies: {request.COOKIES}")
        if request.accepted_renderer.format == "html":
            user = user_service_manager.get_user_from_request(request)
            return response_manager.HTTP_200(
                data=user, template_name=self.template_name
            )
# account/views/user_views.py

# ... (other imports and code remain the same)

class LoginAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "login.html"

    def get(self, request):
        if request.accepted_renderer.format == "html":
            return Response({})
        return Response({"message": "Use POST for login"})

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                if request.accepted_renderer.format == "html":
                    return response_manager.HTTP_400(
                        data=f"Invalid input : {str(serializer.errors)}",
                        template_name=self.template_name,
                    )
                return Response(
                    {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, email=email, password=password)
            print(f"user auth : {user}")
            if not user:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            refresh = RefreshToken.for_user(user)
            token_data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            request.session["token_data"] = token_data
            if request.accepted_renderer.format == "html":
                response = redirect(reverse("home"))
                response.set_cookie(
                    "access_token",
                    token_data["access"],
                    httponly=True,
                    secure=False,  # Change to False for development (use True in production with HTTPS)
                    samesite="Lax",
                    max_age=3600,  # Match ACCESS_TOKEN_LIFETIME (1 hour)
                )
                messages.success(request, "Logged in successfully")
                return response
            return Response(token_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ... (VerifiyOTPAPIView and RegisterAPIView remain the same)

class HomeViewAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "home.html"
    permission_classes = [CustomIsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user  # Use request.user (set by middleware or permission)
        print(f"session {request.session.get('token_data')}")
        print(f"user in home : {user}")
        print(f"Authorization header: {request.META.get('HTTP_AUTHORIZATION')}")
        print(f"Cookies: {request.COOKIES}")
        
        if request.accepted_renderer.format == "html":
            # Removed redundant user re-assignment; use request.user
            return response_manager.HTTP_200(
                data={'user': user},  # Pass a dictionary to avoid 400 error
                template_name=self.template_name
            )
        return Response({"user": UserSerializer(user).data}, status=status.HTTP_200_OK)



# account/views/user_views.py
# ... (other imports and code remain the same)

class LogoutAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "login.html"

    def post(self, request):
        try:
            # Blacklist the refresh token if provided
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            # Clear the session
            request.session.flush()

            # Clear Django's session-based authentication
            logout(request)

            # Log session and cookies for debugging (incoming request cookies)
            print(f"Session after logout: {request.session.get('token_data')}")
            print(f"Cookies after logout: {request.COOKIES}")

            # Prepare the response
            response = Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_205_RESET_CONTENT,
            )

            # Delete the access_token cookie
            response.delete_cookie(
                "access_token",
                path="/"  # Ensure the cookie is deleted for all paths
            )
            # Also clear other cookies to avoid interference
            response.delete_cookie("csrftoken", path="/")
            response.delete_cookie("messages", path="/")

            # Explicitly set access_token to empty with expired max_age
            response.set_cookie(
                "access_token",
                value="",
                max_age=0,
                path="/",
                httponly=True,
                samesite="Lax"
            )

            if request.accepted_renderer.format == "html":
                messages.success(request, "You have been logged out successfully.")
                return redirect(reverse("login"))  # Clean redirect without query params
            return response

        except Exception as e:
            logger.error(
                f"Error during logout: {str(e)}",
                extra={"service": "USER SERVICE"},
                exc_info=True,
            )
            response = Response(
                {"error": "Invalid refresh token or logout failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            response.delete_cookie("access_token", path="/")
            response.delete_cookie("csrftoken", path="/")
            response.delete_cookie("messages", path="/")
            response.set_cookie(
                "access_token",
                value="",
                max_age=0,
                path="/",
                httponly=True,
                samesite="Lax"
            )
            if request.accepted_renderer.format == "html":
                messages.error(request, "Logout failed. Please try again.")
                return redirect(reverse("login"))
            return response

    def get(self, request):
        return self.post(request)