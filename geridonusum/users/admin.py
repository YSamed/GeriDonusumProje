from django.contrib import admin

# Register your models here.
from users.models import Profile , ProfileStatus , Donation 

admin.site.register(Profile)
admin.site.register(ProfileStatus)
admin.site.register(Donation)
