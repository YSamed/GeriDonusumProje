# admin.py

from django.contrib import admin
from .models import RecyclingMaterial , UserRecyclingMaterial

admin.site.register(RecyclingMaterial)
admin.site.register(UserRecyclingMaterial)
