# Generated by Django 5.1.8 on 2025-04-02 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_account_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Mobile'),
        ),
    ]
