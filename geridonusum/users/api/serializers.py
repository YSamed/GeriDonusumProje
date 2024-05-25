from users.models import Profile, ProfileStatus, Donation
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    # Kullanıcı adını okunabilir bir şekilde göstermek için StringRelatedField kullanılır
    user = serializers.StringRelatedField(read_only=True)
    # Kullanıcı resmini değiştirilemez bir şekilde göstermek için ImageField kullanılır
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

class ProfileImageSerializer(serializers.ModelSerializer):
    # Kullanıcı resmini güncellemek için kullanılır
    class Meta:
        model = Profile
        fields = ['image']

class ProfileStatusSerializer(serializers.ModelSerializer):
    # Kullanıcı profiline ait durumları göstermek için kullanılır
    user_profile = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ProfileStatus
        fields = '__all__'

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'
