from rest_framework import serializers
from .models import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'


class CreateFriendRequestSerializer(serializers.Serializer):
    to_user_id = serializers.IntegerField(required=True)
