# Generated by Django 3.2 on 2021-05-18 13:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0013_auto_20210512_1510'),
        ('activitylogs', '0003_alter_activitylog_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitylog',
            name='overlay',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='activity_log_overlay', to='documents.overlay'),
        ),
        migrations.AlterField(
            model_name='activitylog',
            name='page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='activity_log_page', to='documents.page'),
        ),
    ]
