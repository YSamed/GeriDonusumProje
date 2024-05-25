from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, ProfileStatusViewSet, DonationLeaderboardAPIView, make_donation, UserDonationListAPIView, ProfileImageView

router = DefaultRouter()
router.register(r'kullanici-profilleri', ProfileViewSet)
router.register(r'kullanici-durumları', ProfileStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profil_foto/<int:pk>/', ProfileImageView.as_view(), name='profil-foto'),  
    path('donation-leaderboard/', DonationLeaderboardAPIView.as_view(), name='donation-leaderboard'),
    path('make-donation/', make_donation, name='make_donation'),
    path('user-donations/', UserDonationListAPIView.as_view(), name='user-donations'),  
]
