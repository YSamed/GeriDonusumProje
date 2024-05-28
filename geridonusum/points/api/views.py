from rest_framework import generics, status
from rest_framework.response import Response
from ..models import RecyclingMaterial, UserPoints, UserRecyclingMaterial
from .serializers import RecyclingMaterialSerializer, UserPointsSerializer, UserRecyclingMaterialSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

class RecyclingMaterialListCreateAPIView(generics.ListCreateAPIView):
    queryset = RecyclingMaterial.objects.all()
    serializer_class = RecyclingMaterialSerializer
    permission_classes = [IsAdminUser]  # Sadece admin kullanıcılar bu view'e erişebilir.

    def perform_create(self, serializer):
        serializer.save()
class UserRecyclingMaterialCreateAPIView(generics.CreateAPIView):
    serializer_class = UserRecyclingMaterialSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Resim alanının boş olup olmadığını kontrol et
        if 'image' not in request.data or not request.data['image']:
            return Response({'error': 'Resim yüklemeniz gerekiyor.'}, status=status.HTTP_400_BAD_REQUEST)

        # Kullanıcı bilgilerini ekle
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user_recycling_material = serializer.save(user=self.request.user)
        
        # Kullanıcının puanını güncelle
        user_points, created = UserPoints.objects.get_or_create(user=self.request.user)
        user_points.points += user_recycling_material.material.point_value
        user_points.save()

class UserRecyclingMaterialListAPIView(generics.ListAPIView):
    serializer_class = UserRecyclingMaterialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserRecyclingMaterial.objects.filter(user=self.request.user)
    
    


class UserPointsAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserPointsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_points = UserPoints.objects.get_or_create(user=self.request.user)[0]
        return user_points
