from rest_framework import serializers
from ..models import OTP

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        exclude = ['code']

class OTPVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        exclude = ['username']