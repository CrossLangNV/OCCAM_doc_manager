# Generated by Django 3.2.6 on 2021-09-02 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctr', '0003_auto_20210902_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ctrcompany',
            name='companion',
        ),
        migrations.RemoveField(
            model_name='ctrcompany',
            name='legal_form',
        ),
        migrations.RemoveField(
            model_name='ctrcompany',
            name='residence',
        ),
    ]