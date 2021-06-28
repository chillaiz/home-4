from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.functional import empty
from rest_framework import serializers
from .models import Post
from .models import Comment


class CommentTextSerializer(serializers.ModelSerializer):
    # CTS
    class Meta:
        model = Comment
        fields = ' text'.split()


class PostListSerializer(serializers.ModelSerializer):
    # PLS
    comment = CommentTextSerializer(many=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = 'title text create_data comment comment_count'.split()

    def get_comment_count(self, obj):
        return obj.comment.count()


class PostCommentsSerializer(serializers.ModelSerializer):
    # PTS
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = 'title text create_data comments'.split()

    def get_comments(self, obj):
        comm = Comment.objects.filter(post_id=obj.id)
        return CommentTextSerializer(comm, many=True).data


class PostValidateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    text = serializers.TextField()
    create_data = serializers.TextField()


class CommentValidateSerializer(serializers.ModelSerializer):
    text = serializers.TextField()


class UserLoginValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10000)
    password = serializers.CharField(max_length=100)


class UserRegisterValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10000)
    password = serializers.CharField(max_length=100)
    password1 = serializers.CharField(max_length=100)

    def __init__(self, instance=None, data=empty,):
        super().__init__(instance, data,)
        self.cleaned_data = None

    def validate_userename(self, username):
        if User.objects.filter(username=username).count() > 0:
            raise ValidationError("уже есть")

    def clean_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise ValidationError('пароль не совпадает')
        return self.cleaned_data['password']