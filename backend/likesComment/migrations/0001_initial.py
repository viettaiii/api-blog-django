# Generated by Django 5.0.1 on 2024-01-22 08:09

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0011_alter_comment_created_at_alter_comment_updated_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2024, 1, 22, 8, 9, 20, 930012))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2024, 1, 22, 8, 9, 20, 930018))),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
