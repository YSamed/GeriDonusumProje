from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from users.models import Profile, ProfileStatus , Donation 
from users.api.serializers import ProfileSerializer, ProfileStatusSerializer, ProfileImageSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from users.api.permissions import ownProfile, statusOwner
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import models
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import decimal
from points.models import UserPoints



# Özel yetkilendirme sağlayan özel bir token alım görünümü
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        }, status=status.HTTP_200_OK)

# Profil verilerini listeleyen, detaylarını gösteren ve güncelleyen genel bir görünüm kümesi
class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, ownProfile]

# Profil durumlarını listeleme, detaylarını gösterme, oluşturma ve güncelleme görünüm kümesi
class ProfileStatusViewSet(ModelViewSet):
    queryset = ProfileStatus.objects.all()
    serializer_class = ProfileStatusSerializer
    permission_classes = [IsAuthenticated, statusOwner]

    # Yeni bir profil durumu oluştururken, ilişkili kullanıcı profili doğrulanmalıdır
    def perform_create(self, serializer):
        user_profile = self.request.user.profile
        serializer.save(user_profile=user_profile)

# Profil resmini güncelleyen genel bir görünüm
class ProfileImageUpdateViewSet(generics.UpdateAPIView):
    serializer_class = ProfileImageSerializer
    permission_classes = [IsAuthenticated]

    # Görünümün hedef profil nesnesini getirme
    def get_object(self):
        profile_instance = self.request.user.profile
        return profile_instance

    # Profil resmini güncelleyen işlem
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

from django.db.models import Sum

class DonationLeaderboardAPIView(APIView):
    def get(self, request):
        # Kullanıcıları toplam bağış miktarına göre sıralayın
        users = User.objects.all().annotate(total_donation=Sum('donation__amount')).order_by('-total_donation')

        # Sıralanmış kullanıcıları serialize edin
        serialized_users = []
        for user in users:
            # Kullanıcıya ait profili alın
            user_profile = user.profile
            # Kullanıcının maksimum bağış miktarını hesaplayın
            max_donation_amount = user_profile.max_donation_amount

            # Kullanıcıya ait toplam bağış miktarı alanını hesaplayın
            total_donation = sum(donation.amount for donation in Donation.objects.filter(user=user))

            # Sıralı kullanıcıları serialize edin
            serialized_user = {
                'username': user.username,
                'total_donation': total_donation,
                #'max_donation_amount': max_donation_amount,
                
                # Profil resmi veya varsayılan avatar burada eklenir
            }
            serialized_users.append(serialized_user)

        return Response(serialized_users)

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def make_donation(request):
    if request.method == 'POST':
        donation_amount = decimal.Decimal(request.data.get('donation_amount'))
        user = request.user

        # Kullanıcının puanlarını kontrol edin
        try:
            user_points = UserPoints.objects.get(user=user)
        except UserPoints.DoesNotExist:
            return Response({'error': 'Kullanıcının puanları bulunamadı.'}, status=400)

        total_points = user_points.points

        # Kullanıcının yeterli puanı var mı kontrol edin
        if total_points >= donation_amount:
            # Kullanıcının bağış miktarını güncelle
            donation, created = Donation.objects.get_or_create(user=user)
            donation.amount += donation_amount
            donation.save()

            # Kullanıcının toplam puanını azaltın
            user_points.points -= donation_amount
            user_points.save()

            return Response({'message': 'Bağış işlemi başarıyla tamamlandı.'}, status=200)
        else:
            return Response({'error': 'Yetersiz puan.'}, status=400)
    else:
        # Desteklenmeyen istek yöntemi
        return Response({'error': 'Yanlış istek yöntemi.'}, status=405)

