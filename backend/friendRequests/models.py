from django.db import models
from datetime import datetime
from posts.models import User
from django.utils import timezone

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sent_friend_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='received_friend_requests')
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())