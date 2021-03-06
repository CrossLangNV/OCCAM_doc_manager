# Generated by Django 3.2 on 2021-05-18 12:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('documents', '0013_auto_20210512_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranslationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint', models.TextField(blank=True, null=True)),
                ('state', models.CharField(
                    choices=[('Created', 'Created'), ('Waiting', 'Waiting'), ('Started', 'Started'),
                             ('In Progress', 'In Progress'), ('Failed', 'Failed'), ('Success', 'Success')],
                    default='Created', max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('page',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translation_request_page',
                                   to='documents.page')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OcrRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint', models.TextField(blank=True, null=True)),
                ('state', models.CharField(
                    choices=[('Created', 'Created'), ('Waiting', 'Waiting'), ('Started', 'Started'),
                             ('In Progress', 'In Progress'), ('Failed', 'Failed'), ('Success', 'Success')],
                    default='Created', max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ocr_request_page',
                                           to='documents.page')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
