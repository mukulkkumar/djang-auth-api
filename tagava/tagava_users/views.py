from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
)
from .models import MobileOTP

from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    MobileOTPSerializer,
    OTPVerificationSerializer
)

# Create your views here.


class RegisterView(CreateAPIView):
    """
    API for the registration of user
    """
    serializer_class = RegisterSerializer


class ChangePasswordView(UpdateAPIView):
    """
    API for the change password of user
    """
    permission_class = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendOTPView(CreateAPIView):
    """
    API for sending an OTP
    """
    serializer_class = MobileOTPSerializer


class VerifyOTPView(UpdateAPIView):
    """
    API for the verification of OTP
    """
    serializer_class = OTPVerificationSerializer
    model = MobileOTP

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            phone_num = serializer.data.get("phone_num")
            otp_num = serializer.data.get("otp_num")
            valid_time = timezone.now()

            mobile_otp = MobileOTP.objects.filter(
                phone_num=phone_num,
                otp_num=otp_num,
                expiry_time__gte=valid_time,
                is_valid=False).update(is_valid=True)

            if mobile_otp:
                return Response({"detail": "OTP is successfully verified"}, status=status.HTTP_200_OK)

        return Response({"detail": "OTP verification failed"}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    """
    API for Forgot Password
    """
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            user.username = username
            user.set_password(password)
            user.save()
            return Response({"detail": "Password successfully changed."}, status=status.HTTP_200_OK)

        return Response({"detail": "Password is not changed"}, status=status.HTTP_400_BAD_REQUEST)
