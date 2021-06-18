
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def post_view(request):
    return Response(data={'list': 'no post'})