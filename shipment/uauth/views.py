from django.shortcuts import render
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status,generics
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from .role_permission import *
from rest_framework.permissions import IsAuthenticated

from django.http import FileResponse, HttpResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from rest_framework.views import APIView
from .email_service import send_opt_via_email, send_rgain_via_email
from django.shortcuts import get_object_or_404
from .utils import generate_license_key
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import io, os
from django.conf import settings
from datetime import date
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
#from rest_framework_social_oauth2.views import ConvertTokenView
from rest_framework.permissions import AllowAny

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


#new added 31 dec
class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                user = User.objects.get(email=email)
                send_opt_via_email(email)
                return Response({'status': 200 ,'message': 'OTP sent successfully to your registered email.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'status': 404 , 'error': 'This email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            # Get validated data
            email = serializer.validated_data.get('email')
            otp = serializer.validated_data.get('otp')
            password1 = serializer.validated_data.get('password1')

            try:
                user = User.objects.get(email=email)

                # Validate OTP
                if str(user.otp) != str(otp):  # Ensure type consistency
                    return Response({'status': 400 ,'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
                # Reset password
                user.set_password(password1)
                user.otp = None  # Clear OTP
                user.save()

                return Response({'status': 200 , 'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'status': 404 , 'error': 'This email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthenticatedPasswordResetView(APIView):
    def post(self, request):
        serializer = AuthenticatedPasswordResetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Perform user registration
        user = self.perform_create(serializer)

        email = serializer.validated_data.get('email', user.email if user else None)

        try:
            # Send verification email if the user is not verified
            if not user.is_verified:
                self.send_verification_email(email)
            return Response({
                'message': 'User created successfully and OTP sent.',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """
        Handle normal user registration and ensure a role is assigned.
        """
        role = serializer.validated_data.get('role')
        if not role:
            raise ValidationError("Role must be assigned during registration.")
        user = serializer.save(role=role)
        return user

    def send_verification_email(self, email):
        """
        Send a verification email to the user.
        """
        if not email:
            raise ValidationError("Email address is required for verification.")
        # Placeholder for sending the email
        send_rgain_via_email(email)
        
        print(f"Verification email sent to {email}")


class UserLoginView(APIView):
    def post(self, request, format=None):
        # Handle email-password login
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"status": False, "message": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({"status": False, "message": "User account is inactive."}, status=status.HTTP_403_FORBIDDEN)

        if not user.is_verified and not user.is_admin:
            return Response({"status": False, "message": "User account is not verified."}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        role_serializer = RoleTypeSerializer(user.role) if user.role else None
        user_data = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'mobile_number': user.mobile_number,
            'role': role_serializer.data if role_serializer else None,
            'is_verified': user.is_verified,
            'is_admin': user.is_admin,
            'is_org_admin': user.is_org_admin,
        }

        return Response({
            "status": True,
            "message": "Login successful",
            "token": {
                "refresh": str(refresh),
                "access": str(access_token),
            },
            "user": user_data,
        }, status=status.HTTP_200_OK)


#new added 31 dec
User = get_user_model()
# Helper function to generate JWT tokens
def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#4/Jan/25
class GoogleLoginView(APIView):
    def post(self, request, *args, **kwargs):
        auth_code = request.data.get("auth_code")
        if not auth_code:
            return Response({"error": "Authorization code is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Exchange auth_code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": auth_code,
            "client_id": "520618349440-in3h8j5u2e5ick0qcebethd1nlq288jb.apps.googleusercontent.com",
            "client_secret": "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",
            "redirect_uri": "http://127.0.0.1:8000/accounts/google/login/callback/",
            "grant_type": "authorization_code",
        }

        token_response = requests.post(token_url, data=data)
        if token_response.status_code != 200:
            return Response({"error": "Failed to fetch tokens."}, status=status.HTTP_400_BAD_REQUEST)

        tokens = token_response.json()
        id_token = tokens.get("id_token")

        # Step 2: Validate the ID token
        validation_url = "https://oauth2.googleapis.com/tokeninfo"
        validation_response = requests.get(validation_url, params={"id_token": id_token})

        if validation_response.status_code != 200:
            return Response({"error": "Invalid ID token."}, status=status.HTTP_400_BAD_REQUEST)

        user_info = validation_response.json()

        # Step 3: Process the user info (e.g., log in or register)
        email = user_info.get("email")
        if not email:
            return Response({"error": "Invalid user information."}, status=status.HTTP_400_BAD_REQUEST)

        # Handle your user authentication logic here
        return Response({"message": "Google login is valid.", "user": user_info}, status=status.HTTP_200_OK)
      
    
class UserLogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # Blacklist the refresh token
            refresh_token = serializer.validated_data.get('refresh_token')
            RefreshToken(refresh_token).blacklist()
            return Response({"status": True, "message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)





class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] 

class UpdateUserVerificationView(generics.UpdateAPIView):
    serializer_class = UserVerificationSerializer
    permission_classes = [IsAuthenticated, IsSystemOrClientAdmin]  # Only HR users can access this view
    

    def update(self, request, *args, **kwargs):
        user = request.user
        # Check if the user is a PS user using the IsPSUser permission class
        if not IsClientAdministrator().has_permission(request, self):
            return Response({'status': False, 'message': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        # Get the user object to update
        instance = get_object_or_404(User, pk=kwargs.get('pk'))

        # Only allow updating the 'is_verified' field
        if 'is_verified' not in request.data:
            return Response({'status': False, 'message': 'No data provided to update.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the serializer instance with the partial update
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        # Validate and save the serializer
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Return a successful response
        return Response({
            'status': True, 
            'message': 'User verification status updated successfully.', 
            'data': serializer.data
        }, status=status.HTTP_200_OK)


#new added 10-12-2024
class PermissionsViewSet(viewsets.ModelViewSet):
    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsSystemOrClientAdmin, IsClientUserEditAndRead]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role.role_name == "System Administrator":
            return Permissions.objects.all()  # System Admin sees everything
        elif user.role.role_name == "Client Administrator":
            return Permissions.objects.filter(company=user.company)  # Filter by company
        elif user.role.role_name == "Client User (Edit and Read)":
            return Permissions.objects.filter(role=user.role)  # Filter by user role
        return Permissions.objects.none()

#new added
class RoleTypeViewSet(viewsets.ModelViewSet):
    queryset = RoleType.objects.all()
    serializer_class = RoleTypeSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsSystemOrClientAdmin]  # Update permission class here
        else:
            permission_classes = [IsAuthenticated]  # Only authentication required for read actions
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role.role_name == "System Administrator":
            return RoleType.objects.all()  # System Admin sees all Role Types
        elif user.role.role_name == "Client Administrator":
            return RoleType.objects.filter(company=user.company)  # Client Admin sees Role Types related to their company
        return RoleType.objects.none()  # Return no Role Types for other users

class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsPSorAdminUser, IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer