# Generated by Django 5.1.1 on 2024-09-29 00:25

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0012_rename_fecha_nacimiento_usuariosextra_birthdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escultores',
            name='foto_perfil',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='res.cloudinary.com/dq1vfo4c8/image'),
        ),
    ]
