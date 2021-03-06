# Generated by Django 3.1.7 on 2021-03-12 23:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=1000)),
                ('content', models.TextField(blank=True, default='')),
                ('state', models.CharField(choices=[('New', 'New'), ('Waiting on start of layout analysis.', 'Waiting Layout Analysis'), ('Running layout analysis.', 'Running Layout Analysis'), ('Layout analysis completed.', 'Completed Layout Analysis'), ('Waiting on start of OCR.', 'Waiting Ocr'), ('Running OCR.', 'Running Ocr'), ('OCR completed.', 'Completed Ocr')], default='New', max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=200)),
                ('path', models.TextField()),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('deleted', models.BooleanField(default=False)),
                ('image_hash', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_document', to='documents.document')),
            ],
        ),
    ]
