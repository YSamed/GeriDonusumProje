from django.urls import path
from .api.views import RecyclingMaterialListCreateAPIView, UserPointsAPIView, UserRecyclingMaterialCreateAPIView 

urlpatterns = [
    path('materials/', RecyclingMaterialListCreateAPIView.as_view(), name='material-list-create'),
    path('user-points/', UserPointsAPIView.as_view(), name='user-points'),
    path('user-recycling-material/', UserRecyclingMaterialCreateAPIView.as_view(), name='user-recycling-material'),
]
