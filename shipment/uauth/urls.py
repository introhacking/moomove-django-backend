from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import *
from rest_framework.routers  import DefaultRouter

router = DefaultRouter()
router.register(r'Users', UserViewSet)
router.register(r'permissions', PermissionsViewSet)
router.register(r'role-types', RoleTypeViewSet)

urlpatterns = [
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', PasswordResetView.as_view(), name='reset_password'),
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('update-user-verification/<int:pk>/', UpdateUserVerificationView.as_view(), name='update-user-verification'),
    path('authenticated-password-reset/', AuthenticatedPasswordResetView.as_view(), name='authenticated-password-reset'),
    path('auth/google/login/', GoogleLoginView.as_view(), name='google-login'),  # Custom API endpoint for Google login
] + router.urls