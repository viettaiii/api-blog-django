# Generated by Django 5.0.1 on 2024-01-19 09:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 19, 9, 55, 21, 154428)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 19, 9, 55, 21, 154435)),
        ),
    ]
