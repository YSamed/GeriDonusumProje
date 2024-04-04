from users.models import Profile , ProfileStatus
from rest_framework import serializers

class ProfileSeralizer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    image = serializers.ImageField(read_only = True)

    class Meta:
        model = Profile
        fields = '__all__'

class ProfileImageSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Profile
        fields = ['image']

class ProfileStatusSerializer(serializers.ModelSerializer):
    user_profile = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ProfileStatus
        fields = '__all__'

