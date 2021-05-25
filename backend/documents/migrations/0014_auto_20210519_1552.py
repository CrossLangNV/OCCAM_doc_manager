# Generated by Django 3.2 on 2021-05-19 15:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0013_auto_20210512_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='geojson',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='geojson',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
