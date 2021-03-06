# Generated by Django 3.2 on 2021-04-15 11:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
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
            ],
        ),
        migrations.AlterField(
            model_name='document',
            name='state',
            field=models.CharField(choices=[('New', 'New'), ('Waiting on start of layout analysis.', 'Waiting Layout Analysis'), ('Running layout analysis.', 'Running Layout Analysis'), ('Layout analysis completed.', 'Completed Layout Analysis'), ('Waiting on start of OCR.', 'Waiting Ocr'), ('Running OCR.', 'Running Ocr'), ('OCR completed.', 'Completed Ocr')], default='New', max_length=50),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AddField(
            model_name='page',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_page', to='documents.document'),
        ),
    ]
