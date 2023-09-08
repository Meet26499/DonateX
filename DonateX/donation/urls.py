from django.urls import path
from .views import (OTPCreateView, OTPVerificationLoginView,
                    CreateDonationView, DonationListView, DonationVisualizationView)

urlpatterns = [
    path('send-otp/', OTPCreateView.as_view(), name='send-otp'),
    path('login/', OTPVerificationLoginView.as_view(), name='login'),
    path('donation/', CreateDonationView.as_view(), name='donation'),
    path('donation-list/', DonationListView.as_view(), name='donation-list'),
    path('donation-visualization/', DonationVisualizationView.as_view(), name='donation-visualization'),
]