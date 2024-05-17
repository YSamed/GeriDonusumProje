from django.urls import path , include
from .views import ProfileViewSet , ProfileStatusViewSet , ProfileImageUpdateViewSet ,DonationLeaderboardAPIView , make_donation
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'kullanici-profilleri',ProfileViewSet)
router.register(r'kullanici-durumları',ProfileStatusViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('profil_foto/',ProfileImageUpdateViewSet.as_view(),name='profil-foto'),
    path('donation-leaderboard/', DonationLeaderboardAPIView.as_view(), name='donation-leaderboard'),
    path('make-donation/', make_donation, name='make_donation'),

]
