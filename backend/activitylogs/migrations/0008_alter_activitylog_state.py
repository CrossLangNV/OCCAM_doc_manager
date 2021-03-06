# Generated by Django 3.2.6 on 2021-09-24 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activitylogs', '0007_alter_activitylog_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylog',
            name='state',
            field=models.CharField(choices=[('Created', 'Created'), ('Not started', 'Not Started'), ('Classified', 'Classified'), ('Waiting', 'Waiting'), ('Started', 'Started'), ('Processing', 'Processing'), ('Failed', 'Failed'), ('Success', 'Success')], default='Not started', max_length=50),
        ),
    ]
