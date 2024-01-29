from django.db import models
from datetime import datetime
from users.models import User


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('fashion', 'Fashion'),
        ('beauty', 'Beauty'),
        ('travel', 'Travel'),
        ('lifestyle', 'Lifestyle'),
        ('personal', 'Personal'),
        ('tech', 'Tech'),
        ('health', 'Health'),
        ('fitness', 'Fitness'),
        ('wellness', 'Wellness'),
    ]
    title = models.TextField(max_length=255, null=False)
    content = models.TextField(max_length=255, null=False)
    image = models.ImageField(upload_to=upload_to, null=False)
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='fashion',
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
