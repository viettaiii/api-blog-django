# Generated by Django 5.0.1 on 2024-01-22 08:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0007_alter_likepost_created_at_alter_likepost_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likepost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 22, 8, 49, 36, 42621)),
        ),
        migrations.AlterField(
            model_name='likepost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 22, 8, 49, 36, 42626)),
        ),
    ]
