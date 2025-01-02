from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status,generics
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from .role_permission import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
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

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

# key = Fernet.generate_key()
# print(f'Generated Key: {key.decode()}')

# cipher_suite = Fernet(key)


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                User.objects.get(email=email)
                send_opt_via_email(email)
                return Response({'status': 200 ,'message': 'OTP sent successfully to your registered email.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'status': 404 , 'error': 'This email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            otp = serializer.validated_data.get('otp')
            password1 = serializer.validated_data.get('password1')
            password2 = serializer.validated_data.get('password2')
            try:
                user = User.objects.get(email=email)
                if user.otp != otp:
                    return Response({'status': 400 ,'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
                if password1 != password2:
                    return Response({'status': 400 , 'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
                user.set_password(password1)
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
        
        # Perform custom save logic based on the role
        self.perform_create(serializer)
        
        # Send email after successful creation
        email = serializer.validated_data.get('email')
        try:
            user = User.objects.get(email=email)
            send_rgain_via_email(email)
            return Response({
                'message': 'User created successfully and OTP sent.',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User creation failed. Email not found.'}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        user = serializer.save()


# class UserLoginView(generics.GenericAPIView):
#     serializer_class = UserLoginSerializer

#     def post(self, request, format=None):
#         serializer = UserLoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data.get('email')
#         password = serializer.validated_data.get('password')
#         user = authenticate(email=email, password=password)

#         if user is not None:
#             # Check if the user is an admin
#             if user.is_admin:
#                 # Admins bypass role and license checks
#                 token = get_tokens_for_user(user)
#                 role_serializer = RoleTypeSerializer(user.role) if user.role else None

#                 user_data = {
#                     'name': user.name,
#                     'id': user.id,
#                     'email': user.email,
#                     'role': role_serializer.data if role_serializer else None,
#                     'is_verified': user.is_verified,
#                     'is_org_admin': user.is_org_admin,
#                     'is_admin': user.is_admin,
#                 }

#                 return Response({
#                     'status': True,
#                     'token': token,
#                     'message': 'Login Success',
#                     'user': user_data
#                 }, status=status.HTTP_200_OK)

#             # Check if the user is verified
#             if not user.is_verified:
#                 return Response({"status": False, "message": "User Account Freezed!"}, status=status.HTTP_403_FORBIDDEN)

#             # Check if the user has a role and return role info
#             if hasattr(user, 'role') and user.role:
#                 role = user.role
#                 role_serializer = RoleTypeSerializer(role)

#                 user_data = {
#                     'name': user.name,
#                     'id': user.id,
#                     'email': user.email,
#                     'role': role_serializer.data,
#                     'is_verified': user.is_verified,
#                     'is_org_admin': user.is_org_admin,
#                     'is_admin': user.is_admin,
#                 }
#                 token = get_tokens_for_user(user)

#                 return Response({
#                     'status': True,
#                     'token': token,
#                     'message': 'Login Success',
#                     'user': user_data
#                 }, status=status.HTTP_200_OK)
#             else:
#                 return Response(
#                     {"status": False, "message": "User has no role associated."},
#                     status=status.HTTP_403_FORBIDDEN
#                 )
#         else:
#             return Response({'status': False, 'message': 'Email or Password is not Valid'}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request, format=None):
        # Validate user credentials
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"status": False, "message": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({"status": False, "message": "User account is inactive."}, status=status.HTTP_403_FORBIDDEN)

        # Skip is_verified check for admin users
        if not user.is_verified and not user.is_admin:
            return Response({"status": False, "message": "Your account is not verified."}, status=status.HTTP_403_FORBIDDEN)

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Prepare the response data
        role_serializer = RoleTypeSerializer(user.role) if user.role else None
        user_data = {
            'userId': user.id,
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
    

# class PermissionsViewSet(viewsets.ModelViewSet):
#     queryset = Permissions.objects.all()
#     serializer_class = PermissionsSerializer
    
#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'destroy']:
#             permission_classes = [IsAuthenticated, IsSystemOrClientAdmin]
#         else:
#             permission_classes = []
#         return [permission() for permission in permission_classes]

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


# class RoleTypeViewSet(viewsets.ModelViewSet):
#     queryset = RoleType.objects.all()
#     serializer_class = RoleTypeSerializer
    
#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'destroy']:
#             permission_classes = [IsAuthenticated, IsAdminUser]
#         else:
#             permission_classes = []
#         return [permission() for permission in permission_classes]

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

    
# class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     A viewset that provides `list`, `retrieve`, and `delete` actions for Customer.
#     """
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer1
#     permission_classes = [IsAuthenticated]  # Optional: Restrict to authenticated users

#     def get_queryset(self):
#         """
#         Optionally customize the queryset if needed (e.g., filter by user/customer).
#         """
#         return super().get_queryset()

#     def destroy(self, request, *args, **kwargs):
#         """
#         Allow deletion of a customer.
#         """
#         return super().destroy(request, *args, **kwargs)
# class GenerateLicenseKeyView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminUser]
#     serializer_class = LicenseKeyGenerationSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = LicenseKeyGenerationSerializer(data=request.data)
#         if serializer.is_valid():
#             duration = serializer.validated_data['duration']
#             try:
#                 # Generate license key
#                 license_key = generate_license_key()

#                 # Calculate the expiration date based on the duration
#                 if duration == '3':
#                     valid_months = 3
#                 elif duration == '6':
#                     valid_months = 6
#                 elif duration == '12':
#                     valid_months = 12
#                 else:
#                     return Response({"error": "Invalid duration"}, status=status.HTTP_400_BAD_REQUEST)

#                 expiration_date = datetime.now() + timedelta(days=30 * valid_months)

#                 # Create a file with the license details
#                 file_content = f"License Key: {license_key}\nValid Until: {expiration_date.strftime('%Y-%m-%d')}"
#                 cipher_suite = settings.CIPHER_SUITE

#                 # Encrypt the file content
#                 encrypted_content = cipher_suite.encrypt(file_content.encode('utf-8'))

#                 # Create a unique filename for the encrypted file
#                 file_name = f"license_key_{license_key}.txt"

#                 # Save the encrypted file to the media directory
#                 file_path = default_storage.save(f"licenses/{file_name}", ContentFile(encrypted_content))

#                 # Construct the full URL for the saved file
#                 file_url = request.build_absolute_uri(f"/media/{file_path}")

#                 # Optional: Save to LicenseTier model without requiring a tier_id
#                 LicenseTier.objects.create(license_file=file_path)

#                 return Response({"message": "License key generated and saved successfully", "file_url": file_url}, status=status.HTTP_200_OK)

#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CustomerCreationView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminUser]
#     serializer_class = CustomerSerializer

#     def post(self, request, *args, **kwargs):
#         file = request.FILES.get('file')
#         if not file:
#             return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             cipher_suite = settings.CIPHER_SUITE


#             # Read and decrypt file content

#             # Read and decrypt file content
#             encrypted_file_content = file.read()
#             decrypted_file_content = cipher_suite.decrypt(encrypted_file_content).decode('utf-8')
#             print("Decrypted file content:", decrypted_file_content)

#             # Split the content by lines
#             lines = decrypted_file_content.splitlines()

#             # Extract license key and validity date
#             license_key = lines[0].split(': ')[1]  # Assuming format "License Key: <key>"
#             license_valid_upto = pd.to_datetime(lines[1].split(': ')[1]).date()  # Assuming format "Valid Until: <date>"

#             # Process other form data
#             org_name = request.data.get('org_name')
#             org_location = request.data.get('org_location')

#             # Create a Customer instance
#             customer = Customer(
#                 org_name=org_name,
#                 org_location=org_location,
#                 license_key=license_key,
#                 license_valid_upto=license_valid_upto
#             )
#             customer.save()

#             return Response({"message": "Customer created successfully"}, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class LicenseAndCustomerCreationView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminUser]

#     def post(self, request, *args, **kwargs):
#         # Step 1: Generate the license key
#         license_key = generate_license_key()

#         # Step 2: Create LicenseTier with the generated key
#         license_tier_data = request.data.get('license_tier', {})
#         license_tier_data['key'] = license_key  # Set the generated license key

#         license_tier_serializer = LicenseTierSerializer(data=license_tier_data)
#         if license_tier_serializer.is_valid():
#             license_tier = license_tier_serializer.save()

#             # Step 3: Create Customer
#             customer_data = request.data.get('customer', {})
#             customer_data['license_tier'] = license_tier.id  # Associate with created LicenseTier
#             customer_serializer = CustomerSerializer(data=customer_data)

#             if customer_serializer.is_valid():
#                 customer_serializer.save()  # Save Customer
#                 return Response({
#                     "message": "LicenseTier and Customer created successfully",
#                     "license_tier": license_tier_serializer.data,
#                     "customer": customer_serializer.data
#                 }, status=status.HTTP_201_CREATED)

#             return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response(license_tier_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CustomerViewSet(viewsets.ModelViewSet):
#     """
#     A viewset that provides `list`, `retrieve`, `create`, and `delete` actions for Customer.
#     The `create` method also creates a LicenseTier with a generated key.
#     """
#     queryset = Customer.objects.all()
#     permission_classes = [IsAuthenticated, IsAdminUser]

#     def get_serializer_class(self):
#         """
#         Use `CustomerSerializer1` for list and retrieve actions.
#         Use `CustomerSerializer` for create and other actions.
#         """
#         if self.action in ['list', 'retrieve']:
#             return CustomerSerializer1
#         elif self.action in ['create', 'update', 'partial_update']:
#             return CustomerSerializer
#         return super().get_serializer_class()
#     def list(self, request, *args, **kwargs):
#         """
#         Custom response for the list action.
#         """
#         queryset = self.get_queryset()
#         customer_data = []
        
#         for customer in queryset:
#             # Serialize the customer
#             customer_serializer = self.get_serializer(customer)
#             # Extracting license tier information
#             license_tier = customer.license_tier  # Assuming a ForeignKey relationship
            
#             # Prepare the license tier data
#             if license_tier:  # Check if license_tier is not None
#                 license_info = {
#                     "tier_name": license_tier.tier_name,  # Assuming license_tier has tier_name field
#                     "duration": license_tier.duration  # Assuming license_tier has duration field
#                 }
#             else:
#                 license_info = {
#                     "tier_name": None,  # Or you can set a default value or message
#                     "duration": None
#                 }

#             customer_info = {
#                 "id":customer_serializer.data['id'],
#                 "license_tier": license_info,
#                 "customer": {
#                     "org_name": customer_serializer.data['org_name'],
#                     "org_location": customer_serializer.data['org_location']
#                 }
#             }
#             customer_data.append(customer_info)

#         return Response({
#             "message": "Customer list retrieved successfully",
#             "customers": customer_data,
#             "total_count": queryset.count(),
#         }, status=status.HTTP_200_OK)

#     def retrieve(self, request, *args, **kwargs):
#         """
#         Custom response for the retrieve action.
#         """
#         instance = self.get_object()
#         customer_serializer = self.get_serializer(instance)

#         # Extracting license tier information
#         license_tier = instance.license_tier  # Assuming a ForeignKey relationship

#         response_data = {
#             "license_tier": {
#                 "tier_name": license_tier.tier_name,  # Assuming license_tier has tier_name field
#                 "duration": license_tier.duration  # Assuming license_tier has duration field
#             },
#             "customer": {
#                 "org_name": customer_serializer.data['org_name'],
#                 "org_location": customer_serializer.data['org_location']
#             }
#         }

#         return Response({
#             "message": "Customer details retrieved successfully",
#             "customers": response_data
#         }, status=status.HTTP_200_OK)
    
#     def create(self, request, *args, **kwargs):
#         """
#         Create LicenseTier and Customer together.
#         """
#         # Step 1: Generate the license key
#         license_key = generate_license_key()

#         # Step 2: Create LicenseTier with the generated key
#         license_tier_data = request.data.get('license_tier', {})
#         license_tier_data['key'] = license_key  # Set the generated license key

#         license_tier_serializer = LicenseTierSerializer(data=license_tier_data)
#         if license_tier_serializer.is_valid():
#             license_tier = license_tier_serializer.save()

#             # Step 3: Create Customer
#             customer_data = request.data.get('customer', {})
#             customer_data['license_tier'] = license_tier.id  # Associate with created LicenseTier
#             customer_serializer = self.get_serializer(data=customer_data)

#             if customer_serializer.is_valid():
#                 customer_serializer.save()  # Save Customer
#                 return Response({
#                     "message": "LicenseTier and Customer created successfully",
#                     "license_tier": license_tier_serializer.data,
#                     "customer": customer_serializer.data
#                 }, status=status.HTTP_201_CREATED)

#             return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response(license_tier_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def update(self, request, *args, **kwargs):
#         """
#         Update LicenseTier and Customer together.
#         """
#         instance = self.get_object()
#         license_tier = instance.license_tier  # Get the existing LicenseTier

#         # Step 1: Update LicenseTier
#         license_tier_data = request.data.get('license_tier', {})
#         if 'key' in license_tier_data:
#             # Optionally, do not allow updating the key
#             license_tier_data.pop('key')  # Remove key if you don't want to change it

#         license_tier_serializer = LicenseTierSerializer(license_tier, data=license_tier_data, partial=True)
#         if license_tier_serializer.is_valid():
#             license_tier_serializer.save()

#             # Step 2: Update Customer
#             customer_data = request.data.get('customer', {})
#             customer_serializer = self.get_serializer(instance, data=customer_data, partial=True)

#             if customer_serializer.is_valid():
#                 customer_serializer.save()  # Save Customer
#                 return Response({
#                     "message": "LicenseTier and Customer updated successfully",
#                     "license_tier": license_tier_serializer.data,
#                     "customer": customer_serializer.data
#                 }, status=status.HTTP_200_OK)

#             return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response(license_tier_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def partial_update(self, request, *args, **kwargs):
#         """
#         Handle PATCH requests. Delegates to the update method.
#         """
#         return self.update(request, *args, **kwargs)
#     def destroy(self, request, *args, **kwargs):
#         """
#         Allow deletion of a customer.
#         """
#         return super().destroy(request, *args, **kwargs)




class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsPSorAdminUser, IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer