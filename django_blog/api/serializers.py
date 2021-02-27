from rest_framework import serializers


class CustomLikeSerializer(serializers.Serializer):
    csrfmiddlewaretoken = serializers.CharField(max_length=64)
    opinion = serializers.ChoiceField(choices=['like', 'dislike'])
    kind = serializers.ChoiceField(choices=['post', 'comment'])
    id = serializers.IntegerField()


class TagSerializer(serializers.Serializer):
    csrfmiddlewaretoken = serializers.CharField(max_length=64)
    name = serializers.CharField(max_length=80)
