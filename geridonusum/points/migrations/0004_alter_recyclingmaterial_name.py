# Generated by Django 4.2.10 on 2024-04-30 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0003_userrecyclingmaterial_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recyclingmaterial',
            name='name',
            field=models.CharField(choices=[('Kağıt', 'Kağıt'), ('Plastik', 'Plastik'), ('Cam', 'Cam'), ('Metal', 'Metal')], max_length=100),
        ),
    ]
