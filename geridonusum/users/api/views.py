from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import Profile, ProfileStatus, Donation
from users.api.serializers import ProfileSerializer, ProfileStatusSerializer, ProfileImageSerializer ,Donation , DonationSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from users.api.permissions import ownProfile, statusOwner
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
import decimal
from points.models import UserPoints
from users.api.serializers import DonationSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import Donation
import datetime




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

# Bağış sıralama API görünümü
class DonationLeaderboardAPIView(APIView):
    permission_classes = [AllowAny]  # Herkese açık erişim

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
    
class UserDonationListAPIView(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Mevcut oturum açmış kullanıcının yapmış olduğu bağışları getir
        return Donation.objects.filter(user=self.request.user)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_donation(request):
    # Gelen isteğin içeriğini kontrol et
    if 'donation_amount' not in request.data:
        return Response({'error': 'Bağış miktarı belirtilmedi.'}, status=status.HTTP_400_BAD_REQUEST)

    donation_amount = request.data.get('donation_amount')

    # Bağış miktarını decimal cinsine dönüştür
    try:
        donation_amount = decimal.Decimal(donation_amount)
    except decimal.InvalidOperation:
        return Response({'error': 'Geçersiz bağış miktarı.'}, status=status.HTTP_400_BAD_REQUEST)

    # Bağış miktarının pozitif olduğunu kontrol et
    if donation_amount <= 0:
        return Response({'error': 'Bağış miktarı pozitif olmalıdır.'}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user

    # Bağış tarihini al
    donation_date = request.data.get('donation_date')

    # Bağış tarihini kontrol et
    if donation_date:
        try:
            # Bağış tarihini dd.mm.yyyy formatına dönüştür
            donation_date = datetime.datetime.strptime(donation_date, '%d.%m.%Y')
        except ValueError:
            return Response({'error': 'Geçersiz bağış tarihi formatı. Lütfen gg.aa.yyyy formatında girin.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Bağış tarihi verisi yoksa, varsayılan olarak şu anki tarihi kullan
        donation_date = datetime.datetime.now()

    # Kullanıcının puanlarını kontrol et
    try:
        user_points = UserPoints.objects.get(user=user)
    except UserPoints.DoesNotExist:
        return Response({'error': 'Kullanıcının puanları bulunamadı.'}, status=status.HTTP_400_BAD_REQUEST)

    total_points = user_points.points

    # Kullanıcının yeterli puanı var mı kontrol et
    if total_points >= donation_amount:
        # Kullanıcının bağış miktarını güncelle
        donation, created = Donation.objects.get_or_create(user=user)
        donation.amount += donation_amount
        donation.donation_date = donation_date # Bağış tarihini ayarla
        donation.save()

        # Kullanıcının toplam puanını azaltın
        user_points.points -= donation_amount
        user_points.save()

        return Response({'message': 'Bağış işlemi başarıyla tamamlandı.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Yetersiz puan.'}, status=status.HTTP_400_BAD_REQUEST)

class UserDonationListAPIView(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Donation.objects.filter(user=self.request.user)
    

class ProfileImageView(APIView):
    permission_classes = [AllowAny]  # Herkese açık erişim

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Kullanıcı bulunamadı.'}, status=404)

        # Kullanıcıya ait profil nesnesini alın
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            return Response({'error': 'Kullanıcı profili bulunamadı.'}, status=404)

        # Profil nesnesinin resim URL'sini alın
        image_url = profile.image.url if profile.image else None

        # Görüntü URL'sini döndürün
        return Response({'image_url': image_url})

class ProfileImageUpdateViewSet(generics.UpdateAPIView):
    serializer_class = ProfileImageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile