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


class PostCommentsSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = 'title text create_data comments'.split()

    def get_comments(self, obj):
        comm = Comment.objects.filter(post_id=obj.id)
        return CommentTextSerializer(comm, many=True).data