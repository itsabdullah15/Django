# Generated by Django 5.1.3 on 2024-12-29 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0003_cat_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
