# Generated by Django 5.0.1 on 2024-01-22 08:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likesComment', '0002_alter_likecomment_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likecomment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 22, 8, 39, 52, 403300)),
        ),
        migrations.AlterField(
            model_name='likecomment',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 22, 8, 39, 52, 403306)),
        ),
    ]
