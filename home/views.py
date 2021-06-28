import serializers
from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from home.serializers import PostListSerializer, PostCommentsSerializer, PostValidateSerializer, \
    CommentValidateSerializer, UserRegisterValidateSerializer, UserLoginValidateSerializer
from home.models import Post
from home.models import Comment


@api_view(['GET'])
def post_view(request):
    post = Post.objects.all()
    data = PostListSerializer(post, many=True).data
    return Response(data={'list': data})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_view_id(request, id):
    if request.method == 'GET':
        post = Post.objects.get(id=id)
        data = PostListSerializer(post, many=False).data
        return Response(data={'list': data})
    elif request.method == 'POST':
        serializer = PostValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message': 'ERROR',
                    'error': serializer.errors
                }
            )
        post = Post.objects.create(
            title=serializers.validated_data['title'],
            text=serializers.validated_data['text'],
            create_data=serializers.validated_data['create_data']
        )
        post.save()
        return Response()


@api_view(['GET', 'POST'])
def post_view_id_comments(request, id):
    if request.method == 'GET':
        post = Post.objects.get(id=id)
        data = PostCommentsSerializer(post, many=False).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = CommentValidateSerializer(data=request.data)
        if not serializer.is_valid():
                    return Response(
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                        data={
                            'message': 'ERROR',
                            'error': serializer.errors
                        }
                    )
        text = request.data.get('comment', '')
        Comment.objects.create(text=text)
        return Response(data={'message': 'created'})

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
        user = auth.autenticate(username=username, password=password)
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