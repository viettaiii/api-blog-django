# Generated by Django 5.0.1 on 2024-01-22 09:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friendRequests', '0002_friendrequest_delete_friendrequestaa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 22, 9, 55, 25, 209400)),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 22, 9, 55, 25, 209406)),
        ),
    ]