# Generated by Django 5.1.3 on 2025-01-06 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_main_picname2_main_picurl2'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='about_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
