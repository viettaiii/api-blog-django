from rest_framework import serializers
from .models import Post
from comments.serializers import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, required=False)
    class Meta:
        model = Post
        fields = '__all__'


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


class CreatePostSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    content = serializers.CharField(required=True)
    image = serializers.ImageField(required=True)
    category = serializers.ChoiceField(choices=CATEGORY_CHOICES, required=True)
