# Generated by Django 5.1.3 on 2024-12-27 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='profile_photo',
            field=models.ImageField(default='profile_photos/default.jpg', upload_to='profile_photos/'),
        ),
    ]
