# Generated by Django 3.2.3 on 2021-05-31 18:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activitylogs', '0004_auto_20210518_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitylog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
