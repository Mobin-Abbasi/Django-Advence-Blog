from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from .serializers import PostSerializer
from ...models import Post


"""
from rest_framework.decorators import api_view, permission_classes

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.filter(status=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        post.delete()
        return Response(
            {"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )

"""


class PostList(APIView):
    """getting a list of posts and creating new post"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get(self, request):
        """retrieving a list of posts"""
        post = Post.objects.filter(status=True)
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    def post(self, request):
        """creating a post with provided data"""
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PostDetail(APIView):
    """retrieving, updating, or deleting a post"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get(self, request, id):
        """retrieving a post"""
        post = get_object_or_404(Post, id=id)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def put(self, request, id):
        """updating a post with provided data"""
        post = get_object_or_404(Post, id=id)
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        """deleting a post"""
        post = get_object_or_404(post, id=id)
        post.delete()
        return Response(
            {"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
