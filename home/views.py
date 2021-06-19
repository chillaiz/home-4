
from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.serializers import PostListSerializer, CommentTextSerializer, PostCommentsSerializer
from home.models import Post
from home.models import Comment


@api_view(['GET'])
def post_view(request):
    post = Post.objects.all()
    data = PostListSerializer(post, many=True).data
    return Response(data={'list': data})


@api_view(['GET'])
def post_view_id(request, id):
    post = Post.objects.get(id=id)
    data = PostListSerializer(post, many=False).data
    return Response(data={'list': data})


@api_view(['GET'])
def post_view_id_comments(request, id):
    post = Post.objects.get(id=id)
    data = PostCommentsSerializer(post, many=False).data
    return Response(data=data)
