# Generated by Django 3.2.6 on 2021-09-02 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctr', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otherfact',
            name='company',
        ),
        migrations.RemoveField(
            model_name='residence',
            name='company',
        ),
        migrations.RemoveField(
            model_name='scopeofbusiness',
            name='company',
        ),
        migrations.RemoveField(
            model_name='statutoryauthority',
            name='company',
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='companion',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='other_facts',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='residence',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='scope_of_business',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='ctrcompany',
            name='statutory_authorities',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='ctrcompany',
            name='legal_form',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='ctrcompany',
            name='trading_company',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.DeleteModel(
            name='Companion',
        ),
        migrations.DeleteModel(
            name='OtherFact',
        ),
        migrations.DeleteModel(
            name='Residence',
        ),
        migrations.DeleteModel(
            name='ScopeOfBusiness',
        ),
        migrations.DeleteModel(
            name='StatutoryAuthority',
        ),
    ]
