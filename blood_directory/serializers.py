from rest_framework import serializers
from .models import EmergencyRequest, UserProfile, DonationHistory


class EmergencyRequestserializers(serializers.ModelSerializer):
    class Meta:
        model = EmergencyRequest
        fields = '__all__'

class UserProfileserializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class DonationHistoryserializers(serializers.ModelSerializer):
    class Meta:
        model = DonationHistory
        fields = '__all__'