# Generated by Django 5.1.1 on 2024-09-15 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0003_alter_votaciones_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventos',
            old_name='fecha',
            new_name='fecha_inicio',
        ),
        migrations.AddField(
            model_name='eventos',
            name='fecha_final',
            field=models.DateField(null=True),
        ),
    ]
