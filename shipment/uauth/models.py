from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import Permission
from aggregator.models import Clientinfo
# Gender choices for the PersonalDetails model
GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
    ("T", "Other"),
)


class Permissions(models.Model):
    route_path = models.CharField(max_length=28)
    permission_description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.route_path


#new added 23 dec
class RoleType(models.Model):
    SYSTEM_ADMINISTRATOR = 'System Administrator'
    CLIENT_ADMINISTRATION = 'Client Administrator'
    CLIENT_USER_OPERATOR = 'Client User (Edit and Read)'
    CLIENT_USER_READ_ONLY = 'Client User (Read Only)'
    USER='User'


    ROLE_CHOICES = [
        (SYSTEM_ADMINISTRATOR, 'System Administrator'),
        (CLIENT_ADMINISTRATION, 'Client Administrator'),
        (CLIENT_USER_OPERATOR,  'Client User (Edit and Read)'),
        (CLIENT_USER_READ_ONLY, 'Client User (Read Only)'),
        (USER, 'User'),
    ]

    role_name = models.CharField(max_length=255, choices=ROLE_CHOICES)
    #role_description = models.TextField()

    def __str__(self):
        return self.role_name

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, name, password, **extra_fields)

    def create_user_from_google(self, email, name, **extra_fields):
        """
        Creates a user from Google login. 
        No password is set since OAuth handles authentication.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_unusable_password()  # No password is required for Google-authenticated users
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):  # Added PermissionsMixin for Django permissions compatibility
    client = models.ForeignKey(Clientinfo, on_delete=models.CASCADE, null=True, blank=True,default='Grace_20250107173155')
    email = models.EmailField(unique=True, null=False, blank=False, default="placeholder@example.com")
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.ForeignKey('RoleType', on_delete=models.SET_NULL, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_org_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Used for admin panel access
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #new added
    otp = models.CharField(max_length=6, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the given permission. We are only considering superusers here.
        You can extend this to check for specific permissions assigned to this user.
        """
        if self.is_admin:
            return True

        # Implement additional permission logic here, e.g., checking custom permissions
        if self.role and self.role.role_name  == "System Administrator":  # Assuming `RoleType` has a `role_name ` field admin (remove)
            return perm == "can_manage_system"  # Example permission check

        return False

    def has_module_perms(self, app_label):
        """
        Return True if the user has permissions for the given app_label.
        For example, checking if the user has permissions for a specific app.
        """
        if self.is_admin:
            return True

        if self.role and self.role.role_name == "System Administrator":
            if app_label == "uauth":
                return True

        return False

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(RoleType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} - {self.role.role_name}"


class PersonalDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/', null=True, blank=True)
    first_name = models.CharField(max_length=62, null=True, blank=True)
    middle_name = models.CharField(max_length=62, blank=True, null=True)
    last_name = models.CharField(max_length=62, blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=5, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    designation = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name}'s Details"


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=200)
    query_params = models.TextField()
    body = models.TextField()
    status_code = models.IntegerField()
    duration = models.FloatField()  # Time taken in seconds
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.method} {self.path} at {self.timestamp}'
