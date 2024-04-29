# Generated by Django 4.2.10 on 2024-04-29 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('points', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRecyclingMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='points.recyclingmaterial')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]