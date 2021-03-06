# Generated by Django 3.2 on 2021-05-12 09:00

from django.db import migrations, models

import documents.models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0010_auto_20210512_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='state',
            field=models.CharField(
                choices=[('New', 'New'), ('Waiting on start of layout analysis.', 'Waiting Layout Analysis'),
                         ('Running layout analysis.', 'Running Layout Analysis'),
                         ('Layout analysis completed.', 'Completed Layout Analysis'),
                         ('Waiting on start of OCR.', 'Waiting Ocr'), ('Running OCR.', 'Running Ocr'),
                         ('OCR completed.', 'Completed Ocr')], default='New', max_length=50),
        ),
        migrations.AlterField(
            model_name='geojson',
            name='lang',
            field=documents.models.LangField(
                choices=[('NL', 'Nederlands'), ('EN', 'English'), ('FR', 'Français'), ('DE', 'Deutsch')], default='EN',
                max_length=2),
            preserve_default=False,
        ),
    ]
