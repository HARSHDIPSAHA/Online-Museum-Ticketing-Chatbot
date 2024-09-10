from rest_framework import serializers
from .models import CustomUser, Trip
import json

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone_number']

class TripSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Trip
        fields = ['user', 'museum_name', 'visitors_info', 'transaction_id', 'confirmed', 'phone_number']

    def create(self, validated_data):
        validated_data['visitors_info'] = json.dumps(validated_data['visitors_info'])
        return Trip.objects.create(**validated_data)
