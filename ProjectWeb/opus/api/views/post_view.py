from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Post
from ..seraliazers import PostSeraliazer
from rest_framework import generics 

class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSeraliazer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PostSeraliazer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSeraliazer(post)
        return Response(serializer.data)
    
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSeraliazer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TopTenPostListAPIView(generics.ListAPIView):
    queryset = Post.objects.order_by('likes')[:10]
    serializer_class = PostSeraliazer