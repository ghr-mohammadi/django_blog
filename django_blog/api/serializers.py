from rest_framework import serializers

from blog.models import BlogUser


class BlogUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BlogUser
        fields = ['username', 'first_name', 'last_name', 'email']
