from django.contrib import messages
from django.db.models import Model
from django.db.models import F
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomLikeSerializer, TagSerializer
from blog.models import BlogUser, Post, Comment, PostLike, CommentLike, Tag


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

    serialized_data = CustomLikeSerializer(data=request.data)
    if serialized_data.is_valid():
        user_opinion = opinion_dict[serialized_data.validated_data['opinion']]
        model, model_like = get_model_kind(serialized_data.validated_data['kind'])
        try:
            instance = model.objects.get(id=serialized_data.validated_data['id'])
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
                instance.refresh_from_db()
                return Response(data={'delete': 'delete', 'like': instance.like_qty, 'dislike': instance.dislike_qty}, status=status.HTTP_200_OK)
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
                instance.refresh_from_db()
                return Response(data={'update': 'update', 'like': instance.like_qty, 'dislike': instance.dislike_qty}, status=status.HTTP_200_OK)
        except model_like.DoesNotExist:
            instance_like = model_like.objects.create(user=user, instance=instance, value=user_opinion)
            if user_opinion:
                instance.like_qty = F('like_qty') + 1
            else:
                instance.dislike_qty = F('dislike_qty') + 1
            instance.save()
            instance.refresh_from_db()
            return Response(data={'create': 'create', 'like': instance.like_qty, 'dislike': instance.dislike_qty}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['Post'])
def create_tag(request):
    try:
        user = BlogUser.objects.get(id=request.user.id)
    except BlogUser.DoesNotExist:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    serialized_data = TagSerializer(data=request.data)
    if serialized_data.is_valid() and user.has_perm('blog.add_post'):
        name = serialized_data.validated_data['name']
        tag = Tag.objects.create(creator=user, name=name)
        messages.success(request, 'تگ مورد نظر شما با موفقیت ثبت شد.')
        return Response(status=status.HTTP_201_CREATED)
    messages.error(request, 'متاسفانه در مراحل ثبت تگ در خواستی شما خطایی به وجود آمده است.')
    return Response(status=status.HTTP_400_BAD_REQUEST)
