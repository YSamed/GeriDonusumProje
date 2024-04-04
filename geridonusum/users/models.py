from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    bio = models.CharField(max_length=200,blank=True,null=True)
    city = models.CharField(max_length=200,blank=True,null=True)
    image = models.ImageField(null=True,blank=True,upload_to='profile_images/%Y/%m/')

    def __str__(self):
        return self.user.username
    

    class Meta:
        verbose_name_plural = 'Kullanıcılar'

    
    def save (self,*args,**kwargs):
        super().save(*args , **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 600 or img.width > 600:
                output_size = (600,600)
                img.thumbnail(output_size)
                img.save(self.image.path)

    
class ProfileStatus(models.Model):
    user_profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    status_message = models.CharField(max_length=250)
    creation_date = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user_profile)
    
    class Meta:
        verbose_name_plural = 'Kullanıcı Mesajları'
        
