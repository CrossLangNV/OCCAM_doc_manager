# Generated by Django 3.2.6 on 2021-09-13 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0030_document_oaipmh_item_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='oaipmh_item_url',
            field=models.URLField(default=''),
        ),
    ]