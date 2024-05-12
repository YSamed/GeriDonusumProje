from rest_framework import serializers
from ..models import RecyclingMaterial, UserPoints, UserRecyclingMaterial
from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import RecyclingMaterial, UserPoints, UserRecyclingMaterial
from django.contrib.auth.models import User


class RecyclingMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecyclingMaterial
        fields = ['id', 'name', 'point_value']

class UserPointsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = UserPoints
        fields = ['user', 'points']
        read_only_fields = ['points']

    def get_user(self, obj):
        return obj.user.username

class UserRecyclingMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecyclingMaterial
        fields = ['user', 'material', 'image']
