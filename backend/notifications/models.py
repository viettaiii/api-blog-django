from django.db import models
from datetime import datetime
from users.models import User


class Notification(models.Model):
    title = models.CharField(max_length=255, null=False)
    content = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())