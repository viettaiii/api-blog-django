from rest_framework import serializers
from .models import LikeComment


class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = '__all__'


class CreateLikeCommentSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField(required=True)
