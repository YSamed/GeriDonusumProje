# points/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import RecyclingMaterial, UserPoints, UserRecyclingMaterial
from .serializers import RecyclingMaterialSerializer, UserPointsSerializer, UserRecyclingMaterialSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

class RecyclingMaterialListCreateAPIView(generics.ListCreateAPIView):
    queryset = RecyclingMaterial.objects.all()
    serializer_class = RecyclingMaterialSerializer
    permission_classes = [IsAuthenticated]

class UserPointsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_points = UserPoints.objects.get_or_create(user=request.user)[0]
        serializer = UserPointsSerializer(user_points)
        return Response(serializer.data)

    def post(self, request):
        user_points = UserPoints.objects.get_or_create(user=request.user)[0]
        points = request.query_params.get('points')
        user_points.points += int(points)
        user_points.save()
        serializer = UserPointsSerializer(user_points)
        return Response(serializer.data)

class UserRecyclingMaterialCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        material_id = request.data.get('material')
        material = RecyclingMaterial.objects.get(id=material_id)
        UserRecyclingMaterial.objects.create(user=request.user, material=material)
        
        # Kullanıcının puanını arttır
        user_points = UserPoints.objects.get_or_create(user=request.user)[0]
        user_points.points += material.point_value
        user_points.save()
        
        serializer = UserPointsSerializer(user_points)
        return Response(serializer.data)
