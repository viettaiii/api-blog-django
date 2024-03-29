# Generated by Django 5.0.1 on 2024-01-26 04:59

import datetime
import posts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_alter_post_created_at_alter_post_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 26, 4, 59, 21, 140088)),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to=posts.models.upload_to),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 26, 4, 59, 21, 140099)),
        ),
    ]
