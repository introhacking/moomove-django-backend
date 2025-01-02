from rest_framework import serializers
from uauth.models import User
from .models import *

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    password1 = serializers.CharField(max_length=128, write_only=True)
    password2 = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = ['id', 'route_path', 'permission_description']

class RoleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleType
        fields = ['id', 'role_name', 'role_description']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    role = RoleTypeSerializer()
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'mobile_number', 'password', 'password2', 'role', 'is_verified']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        role_data = validated_data.pop('role')
        role = RoleType.objects.create(**role_data)
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
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
