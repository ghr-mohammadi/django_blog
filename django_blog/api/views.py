from django.db.models import Model
from django.db.models import F
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomLikeSerializer
from blog.models import BlogUser, Post, Comment, PostLike, CommentLike


def get_model_kind(kind: str) -> Model:
    if kind == 'post':
        return Post, PostLike
    elif kind == 'comment':
        return Comment, CommentLike
    else:
        return None


@api_view(['Post'])
def opinion(request):
    opinion_dict = {'like': True, 'dislike': False}
    try:
        user = BlogUser.objects.get(id=request.user.id)
    except BlogUser.DoesNotExist:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer = CustomLikeSerializer(data=request.data)
    if serializer.is_valid():
        user_opinion = opinion_dict[serializer.validated_data['opinion']]
        model, model_like = get_model_kind(serializer.validated_data['kind'])
        try:
            instance = model.objects.get(id=serializer.validated_data['id'])
        except model.DoesNotExist:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            instance_like = model_like.objects.get(user=user, instance=instance)
            if instance_like.value == user_opinion:
                instance_like.delete()
                if user_opinion:
                    instance.like_qty = F('like_qty') - 1
                else:
                    instance.dislike_qty = F('dislike_qty') - 1
                instance.save()
                return Response(data={'name': 'reza'}, status=status.HTTP_200_OK)
            else:
                instance_like.value = user_opinion
                instance_like.save()
                if user_opinion:
                    instance.like_qty = F('like_qty') + 1
                    instance.dislike_qty = F('dislike_qty') - 1
                else:
                    instance.like_qty = F('like_qty') - 1
                    instance.dislike_qty = F('dislike_qty') + 1
                instance.save()
                return Response(data={'name': 'ali'}, status=status.HTTP_200_OK)
        except model_like.DoesNotExist:
            instance_like = model_like.objects.create(user=user, instance=instance, value=user_opinion)
            if user_opinion:
                instance.like_qty = F('like_qty') + 1
            else:
                instance.dislike_qty = F('dislike_qty') + 1
            instance.save()
            return Response(data={'name': 'gholamreza'}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
