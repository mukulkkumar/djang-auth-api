from django.urls import path, re_path, include
from rest_framework_simplejwt import views as jwt_views
from .views import (
    RegisterView,
    ChangePasswordView,
    SendOTPView,
    VerifyOTPView,
    ForgotPasswordView,
)
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/token/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    re_path(r'^', include(router.urls)),
]
