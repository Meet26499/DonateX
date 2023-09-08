from rest_framework import serializers
from ..models import Donation

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['amount']

class DonationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        exclude = ['user']
