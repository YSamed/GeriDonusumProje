

from django.contrib import admin
from .models import RecyclingMaterial, UserPoints

@admin.register(RecyclingMaterial)
class RecyclingMaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'point_value']

@admin.register(UserPoints)
class UserPointsAdmin(admin.ModelAdmin):
    list_display = ['user', 'points']
