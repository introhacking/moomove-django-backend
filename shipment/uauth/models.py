from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

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


class RoleType(models.Model):
    role_name = models.CharField(max_length=50)
    role_description = models.TextField(null=True, blank=True)
    role_permissions = models.ManyToManyField(Permissions)

    def __str__(self) -> str:
        return self.role_name


class UserManager(BaseUserManager):
    def create_user(self, name, role, email=None, mobile_number=None, password=None):
        if not email and not mobile_number:
            raise ValueError('Either email or mobile number must be set')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            role=role,
            mobile_number=mobile_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, role=None, email=None, mobile_number=None, password=None):
        user = self.create_user(
            email=email,
            mobile_number=mobile_number,
            password=password,
            name=name,
            role=role,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
        null=True,
        default=None,
        blank=False
    )
    name = models.CharField(max_length=200)
    mobile_number = models.CharField(unique=True, max_length=20, null=True, blank=True)
    role = models.ForeignKey(RoleType, on_delete=models.CASCADE, null=True, blank=True)
    otp = models.IntegerField(default=0)
    is_org_admin = models.BooleanField(default=False)
    is_password_freezed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email if self.email else self.mobile_number

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


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
