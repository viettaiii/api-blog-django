from rest_framework import serializers
from .models import LikePost


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = '__all__'


class CreateLikePostSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(required=True)
