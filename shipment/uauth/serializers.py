from rest_framework import serializers
from uauth.models import User
from .models import *
import requests
from django.contrib.auth import get_user_model



# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

# class PasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     otp = serializers.IntegerField()
#     password1 = serializers.CharField(max_length=128, write_only=True)
#     password2 = serializers.CharField(max_length=128, write_only=True)

#     def validate(self, data):
#         if data['password1'] != data['password2']:
#             raise serializers.ValidationError("Passwords do not match.")
#         return data


User = get_user_model()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    password1 = serializers.CharField(max_length=128, write_only=True)
    password2 = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        # Validate that passwords match
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")

        # Validate that the email exists
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        # Validate OTP
        if str(user.otp) != str(data['otp']):  # Ensure OTP matches
            raise serializers.ValidationError("Invalid OTP provided.")

        return data

    def save(self):
        # Reset password and clear OTP
        email = self.validated_data['email']
        password = self.validated_data['password1']

        user = User.objects.get(email=email)
        user.set_password(password)
        user.otp = None  # Clear OTP after successful reset
        user.save()

        return user

class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = ['id', 'route_path', 'permission_description']

#new added 23 dec
class RoleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleType
        fields = ['id', 'role_name']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    role = serializers.PrimaryKeyRelatedField(queryset=RoleType.objects.all())  # Use primary key for role assignment
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'mobile_number', 'password', 'password2', 'role', 'is_verified']

    def validate(self, attrs):
        # Ensure passwords match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        # Pop the role data to create the role separately
        role_data = validated_data.pop('role')
        
        # Validate passwords match
        password = validated_data.get('password')
        password2 = validated_data.get('password2')

        if password != password2:
             raise serializers.ValidationError("Passwords do not match.")

        # Create the RoleType object
        role = RoleType.objects.get(id=role_data.id)  # Fetch the role by id

        # Create the user
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=password,
            mobile_number=validated_data.get('mobile_number'),
            role=role
        )
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs

    def save(self, **kwargs):
        try:
            return {"status": True}
        except Exception as e:
            return {"error": str(e)}

class AuthenticatedPasswordResetSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        data['email'] = user.email
        return data

    def validate_password2(self, value):
        if 'password1' in self.initial_data:
            password1 = self.initial_data['password1']
            if password1 != value:
                raise serializers.ValidationError("Passwords do not match.")
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['password1'])
        user.save()

class UserVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_verified']
        read_only_fields = ['id']

# [ GOOGLE ]
class GoogleLoginSerializer(serializers.Serializer): 
    google_id_token = serializers.CharField()

    def validate(self, attrs):
        google_id_token = attrs.get('google_id_token')

        # Send a request to Google to verify the token
        response = requests.post(
            'https://oauth2.googleapis.com/tokeninfo?id_token=' + google_id_token
        )

        if response.status_code != 200:
            raise serializers.ValidationError("Invalid Google ID Token.")

        user_info = response.json()

        # Extract necessary information from Google response (such as email, name)
        google_email = user_info.get('email')
        google_name = user_info.get('name')

        # Check if the user already exists
        user = User.objects.filter(email=google_email).first()

        if not user:
            # If user doesn't exist, create a new user without a password
            user = User.objects.create_user_from_google(
                email=google_email,
                name=google_name
            )

            # Optionally, you can assign a default role here
            default_role = RoleType.objects.filter(role_name="User").first()  # assuming "user" is a default role
            user.role = default_role
            user.save()

        attrs['user'] = user  # Update to 'user' instead of 'User'
        return attrs


# class GoogleLoginSerializer(serializers.Serializer): 
#     google_id_token = serializers.CharField()

#     def validate(self, attrs):
#         google_id_token = attrs.get('google_id_token')

#         # Send a request to Google to verify the token
#         response = requests.post(
#             'https://oauth2.googleapis.com/tokeninfo?id_token=' + google_id_token
#         )

#         if response.status_code != 200:
#             raise serializers.ValidationError("Invalid Google ID Token.")

#         user_info = response.json()

#         # Extract necessary information from Google response (such as email, name)
#         google_email = user_info.get('email')
#         google_name = user_info.get('name')

#         # Check if the user already exists
#         user = User.objects.filter(email=google_email).first()

#         if not user:
#             # If user doesn't exist, create a new user without a password
#             user = User.objects.create_user_from_google(
#                 email=google_email,
#                 name=google_name
#             )

#             # Optionally, you can assign a default role here
#             default_role = RoleType.objects.filter(role_name="User").first()  # assuming "user" is a default role
#             user.role = default_role
#             user.save()

#         attrs['user'] = user  # Update to 'user' instead of 'User'
#         return attrs


# [ 11/03/2025]
class ClientSwitchSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()

    def validate_client_id(self, value):
        try:
            Clientinfo.objects.get(client_id=value)
        except Clientinfo.DoesNotExist:
            raise serializers.ValidationError("Client with given ID does not exist.")
        return value

    def update(self, instance, validated_data):
        client_id = validated_data.get('client_id')
        client = Clientinfo.objects.get(client_id=client_id)
        instance.current_client = client
        instance.save()
        return instance 