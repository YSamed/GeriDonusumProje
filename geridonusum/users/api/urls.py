from django.urls import path , include
from users.api.views import ProfileViewSet , ProfileStatusViewSet , ProfileImageUpdateViewSet 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'kullanici-profilleri',ProfileViewSet)
router.register(r'kullanici-durumları',ProfileStatusViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('profil_foto/',ProfileImageUpdateViewSet.as_view(),name='profil-foto'),
]
