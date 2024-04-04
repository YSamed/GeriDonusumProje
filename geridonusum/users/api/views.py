from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import Profile , ProfileStatus
from users.api.serializers import ProfileSeralizer , ProfileStatusSerializer ,ProfileImageSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from users.api.permissions import ownProfile , statusOwner

class ProfileViewSet(
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    GenericViewSet,
):
    queryset = Profile.objects.all()
    serializer_class = ProfileSeralizer
    permission_classes = [IsAuthenticated , ownProfile]
    

class ProfileStatusViewSet(ModelViewSet):
    queryset = ProfileStatus.objects.all()
    serializer_class = ProfileStatusSerializer
    permission_classes = [IsAuthenticated , statusOwner]

    def perform_create(self, serializer):
        user_profile = self.request.user.profile
        serializer.save(user_profile = user_profile)

class ProfileImageUpdateViewSet(generics.UpdateAPIView):
    serializer_class = ProfileImageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile_nesnesi = self.request.user.profile
        return profile_nesnesi