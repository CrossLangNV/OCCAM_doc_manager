# Generated by Django 3.2.6 on 2021-09-06 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0025_document_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='europeana_item_id',
            field=models.CharField(default='', max_length=1000),
        ),
    ]