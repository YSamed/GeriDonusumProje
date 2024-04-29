# points/serializers.py

from rest_framework import serializers
from .models import RecyclingMaterial, UserPoints, UserRecyclingMaterial
from django.contrib.auth.models import User

class RecyclingMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecyclingMaterial
        fields = ['id', 'name', 'point_value']

class UserPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoints
        fields = ['user', 'points']

class UserRecyclingMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecyclingMaterial
        fields = ['user', 'material']
