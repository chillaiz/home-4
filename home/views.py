import serializers
from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from home.serializers import PostListSerializer, PostCommentsSerializer, PostValidateSerializer, \
    CommentValidateSerializer, UserRegisterValidateSerializer, UserLoginValidateSerializer
from home.models import Post, IsLike
from home.models import Comment



@api_view(['GET'])
def post_view(request):
    post = Post.objects.all()
    data = PostListSerializer(post, many=True).data
    return Response(data={'list': data})

@api_view(['GET', 'POST'])
def post_view_id(request):
    if request.method == "POST":

        serializer = PostValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message': 'ERROR',
                    'errors': serializer.errors
                }
            )
        post = Post.objects.create(
            title=request.validated_data["title"],
            text=request.validated_data["text"],
            like_count=serializer.validated_data['favourite_count'],
        )
        post.hash_tag.set(serializer.validated_data['tags'])
        post.save()
        return Response(data={'message': 'created'})
    else:
        posts = Post.objects.all()
        data = PostListSerializer(posts, many=True, context={"request": request}).data
        return Response(data={'list': data})


@api_view(['GET'])
def post_view_id_comments(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        raise NotFound('Not found')
    if request.method == 'GET':
        data = PostListSerializer(post, many=False).data
        return Response(data=data)
    elif request.method == 'POST':
        IsLike.objects.create(post=post,
                              user=request.user)
        return Response(data={'message': 'Post was liked'})


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'massage': "error",
                    'errors': serializer.errors
                }
            )
        username = request.data['username']
        password = request.data['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            try:
                token = Token.objects.get_or_create(user=user)
            except:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        else:
            return Response(data={'massege': 'USER NOT FOUND'})


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserRegisterValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'massage': "error",
                    'errors': serializer.errors
                }
            )
        User.objects.create_user(
            username=request.data['username'],
            email='a@n.ru',
            password=request.data['password']
        )
        return Response(data={'User created'})
