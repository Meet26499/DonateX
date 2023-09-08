# views.py
from rest_framework import generics, status
from django.contrib.auth import get_user_model, login
from django.http import JsonResponse
from ..models import OTP
from ..serializers import OTPSerializer, OTPVerificationSerializer
from helper import send_otp
import random

class OTPCreateView(generics.CreateAPIView):
    queryset = OTP.objects.all()
    serializer_class = OTPSerializer

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        username = request.data.get('username')
        if phone_number:
            otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            OTP.objects.create(phone_number=phone_number, code=otp_code, username=username)

            # Function to send otp using Twilio
            send_otp(phone_number, otp_code)

            return JsonResponse({'message': 'OTP sent successfully'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        

class OTPVerificationLoginView(generics.CreateAPIView):
    queryset = OTP.objects.all()
    serializer_class = OTPVerificationSerializer

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        user_otp = request.data.get('code')

        if phone_number and user_otp:
            # Verifying the OTP
            otp_record = OTP.objects.filter(phone_number=phone_number, code=user_otp).first()

            if otp_record:
                user, created = get_user_model().objects.get_or_create(phone_number=otp_record.phone_number)

                # Login User with phone number here
                login(request, user)
                return JsonResponse({'message': 'OTP verified and user logged in successfully'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'OTP verification failed'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error': 'Invalid phone number or OTP'}, status=status.HTTP_400_BAD_REQUEST)

