# Generated by Django 3.2.6 on 2021-09-02 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctr', '0002_auto_20210902_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctrcompany',
            name='business_name',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='file_reference',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='legal_status',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='lien',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='location',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='manager',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='number_of_members',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='object_of_business',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='representation',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='share',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='share_capital',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='shareholder',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='shareholders',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='statutory_body',
            field=models.TextField(blank=True, default=''),
        ),
    ]
