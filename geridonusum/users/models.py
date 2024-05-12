from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Bir kullanıcıya bir profil bağlanacak
    image = models.ImageField(null=True, blank=True, upload_to='profile_images/%Y/%m/')  # Kullanıcı resmi

    def __str__(self):
        return self.user.username  # Profili temsil eden string

    class Meta:
        verbose_name_plural = 'Kullanıcılar'  # Django admin arayüzünde görünen modelin ismi

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            # Profil resmi yüklendiyse, boyutunu kontrol et ve yeniden boyutlandır
            img = Image.open(self.image.path)
            if img.height > 600 or img.width > 600:
                output_size = (600, 600)
                img.thumbnail(output_size)
                img.save(self.image.path)

    
class ProfileStatus(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Bir profil için birden fazla durum mesajı
    status_message = models.CharField(max_length=250)  # Durum mesajı
    creation_date = models.DateTimeField(auto_now_add=True)  # Durum mesajının oluşturulma tarihi
    date_update = models.DateTimeField(auto_now=True)  # Durum mesajının son güncellenme tarihi

    def __str__(self):
        return str(self.user_profile)  # Profili temsil eden string

    class Meta:
        verbose_name_plural = 'Kullanıcı Mesajları'  # Django admin arayüzünde görünen modelin ismi
