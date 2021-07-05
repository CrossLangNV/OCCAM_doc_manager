# Generated by Django 3.2 on 2021-04-30 13:06
from django.contrib.auth.models import User
from django.db import migrations

from tutorial.models import UserTutorial


def create_models_if_not_exist(apps, schema_editor):
    for user in User.objects.all():
        UserTutorial.objects.update_or_create(user=user)
        print("created model for user, ", user.email)


class Migration(migrations.Migration):
    dependencies = [
        ('tutorial', '0001_initial'),
    ]

    operations = [migrations.RunPython(create_models_if_not_exist)]