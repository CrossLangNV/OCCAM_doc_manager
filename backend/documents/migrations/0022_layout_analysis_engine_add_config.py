# Generated by Django 3.2.4 on 2021-06-29 15:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0021_alter_document_layout_analysis_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='layoutanalysismodel',
            old_name='value',
            new_name='description',
        ),
        migrations.AddField(
            model_name='layoutanalysismodel',
            name='config',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
