# Generated by Django 5.1.8 on 2025-04-02 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='job_title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Job Title'),
        ),
    ]
