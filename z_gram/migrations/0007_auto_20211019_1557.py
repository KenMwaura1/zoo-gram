# Generated by Django 3.2.8 on 2021-10-19 15:57

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('z_gram', '0006_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpost',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]