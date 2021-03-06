# Generated by Django 3.2.6 on 2021-09-10 09:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0029_alter_document_europeana_item_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200)),
                ('creator', models.CharField(default='', max_length=200)),
                ('subject', models.CharField(default='', max_length=200)),
                ('description', models.CharField(default='', max_length=200)),
                ('publisher', models.CharField(default='', max_length=200)),
                ('contributor', models.CharField(default='', max_length=200)),
                ('date', models.CharField(default='', max_length=200)),
                ('type', models.CharField(default='', max_length=200)),
                ('format', models.CharField(default='', max_length=200)),
                ('identifier', models.CharField(default='', max_length=200)),
                ('source', models.CharField(default='', max_length=200)),
                ('language', models.CharField(default='', max_length=200)),
                ('relation', models.CharField(default='', max_length=200)),
                ('coverage', models.CharField(default='', max_length=200)),
                ('right', models.CharField(default='', max_length=200)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_metadata', to='documents.page')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
