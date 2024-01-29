from rest_framework import serializers
from .models import Comment
# from .serializers import CommentSerializer


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'post',
            'user',
            'parent',
            'replies',
        )

    def get_replies(self, obj):
        replies_qs = Comment.objects.filter(parent=obj)
        replies_serializer = self.__class__(replies_qs, many=True)
        return replies_serializer.data


class CreateCommentSerializer(serializers.Serializer):
    content = serializers.CharField(required=True)
    post_id = serializers.IntegerField(required=True)

class ReplyCommentSerializer(serializers.Serializer):
    content = serializers.CharField(required=True)
    comment_id = serializers.IntegerField(required=True)

class UpdateCommentSerializer(serializers.Serializer):
    content = serializers.CharField(required=True)
