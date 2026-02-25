from rest_framework import serializers
from .models import RewardProfile, RewardHistory


class RewardProfileserializers(serializers.ModelSerializer):
    class Meta:
        model = RewardProfile
        fields = '__all__'

class RewardHistoryserializers(serializers.ModelSerializer):
    class Meta:
        model = RewardHistory
        fields = '__all__'
