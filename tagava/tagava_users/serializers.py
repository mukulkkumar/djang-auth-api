from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MobileOTP
from .helpers import send_otp
import random


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class MobileOTPSerializer(serializers.ModelSerializer):
    """
    Serializer for send otp endpoint
    """
    class Meta:
        model = MobileOTP
        fields = '__all__'

    def create(self, validated_data):
        otp = MobileOTP()
        otp_num = random.randint(1000, 9999)
        phone_num = validated_data['phone_num']

        response = send_otp(otp_num, phone_num)
        if response:
            if response.status_code == 200:
                otp = MobileOTP(
                    phone_num=phone_num,
                    otp_num=otp_num
                )
                otp.save()
        return otp


class OTPVerificationSerializer(serializers.Serializer):
    """
    Serializer for the verification of otp
    """
    phone_num = serializers.CharField(required=True)
    otp_num = serializers.CharField(required=True)

