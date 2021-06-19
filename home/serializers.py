from rest_framework import serializers
from .models import Post
from .models import Comment


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ' text'.split()
