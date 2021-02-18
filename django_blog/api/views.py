from .serializers import BlogUserSerializer
from blog.models import BlogUser
from rest_framework.generics import ListAPIView


class BlogUserList(ListAPIView):
    queryset = BlogUser.objects.all()
    serializer_class = BlogUserSerializer
