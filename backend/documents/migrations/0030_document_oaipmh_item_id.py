# Generated by Django 3.2.6 on 2021-09-13 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0029_alter_document_europeana_item_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='oaipmh_item_id',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]