from django.contrib import admin
from .models import OTP, Donation

# Register your models here.
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_number', 'code']

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status']