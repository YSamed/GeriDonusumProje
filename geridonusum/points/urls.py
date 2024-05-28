from django.urls import path
from .api.views import RecyclingMaterialListCreateAPIView, UserPointsAPIView, UserRecyclingMaterialCreateAPIView, UserRecyclingMaterialListAPIView

urlpatterns = [
    path('materials/', RecyclingMaterialListCreateAPIView.as_view(), name='material-list-create'),
    path('user-points/', UserPointsAPIView.as_view(), name='user-points'),
    path('user-recycling-material/', UserRecyclingMaterialCreateAPIView.as_view(), name='user-recycling-material'),
    path('user-recycling-material-list/', UserRecyclingMaterialListAPIView.as_view(), name='user-recycling-material-list'),  # Yeni eklenen URL
]
