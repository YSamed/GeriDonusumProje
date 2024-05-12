from django.db import models
from django.contrib.auth.models import User

# models.py

from django.db import models

class RecyclingMaterial(models.Model):
    name = models.CharField(max_length=100)
    point_value = models.IntegerField()

    def __str__(self):
        return self.name

class UserPoints(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.points} points"

class UserRecyclingMaterial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(RecyclingMaterial, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='recycling_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.material.name}"
