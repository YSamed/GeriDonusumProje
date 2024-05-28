from rest_framework import serializers
from ..models import RecyclingMaterial, UserPoints, UserRecyclingMaterial
from django.contrib.auth.models import User

class RecyclingMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecyclingMaterial
        fields = ['id', 'name', 'point_value']

class UserPointsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserPoints
        fields = ['user', 'points']
        read_only_fields = ['points']



class UserRecyclingMaterialSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserRecyclingMaterial
        fields = ['user', 'material', 'image']