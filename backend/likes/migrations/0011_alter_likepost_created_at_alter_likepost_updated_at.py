# Generated by Django 5.0.1 on 2024-01-26 05:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0010_alter_likepost_created_at_alter_likepost_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likepost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 26, 5, 1, 18, 611577)),
        ),
        migrations.AlterField(
            model_name='likepost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 26, 5, 1, 18, 611583)),
        ),
    ]
