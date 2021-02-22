from django import template
from ..models import PostLike, CommentLike

register = template.Library()


@register.filter
def post_like(user, post):
    instance = PostLike.objects.filter(user=user, instance=post)
    # return '' if not bool(instance) else ('active' if instance[0].value else '')
    if instance:
        if instance[0].value:
            return ' active'
        else:
            return ''
    else:
        return ''


@register.filter
def post_dislike(user, post):
    instance = PostLike.objects.filter(user=user, instance=post)
    if instance:
        if instance[0].value:
            return ''
        else:
            return ' active'
    else:
        return ''


@register.filter
def comment_like(user, comment):
    instance = CommentLike.objects.filter(user=user, instance=comment)
    if instance:
        if instance[0].value:
            return ' active'
        else:
            return ''
    else:
        return ''


@register.filter
def comment_dislike(user, comment):
    instance = CommentLike.objects.filter(user=user, instance=comment)
    if instance:
        if instance[0].value:
            return ''
        else:
            return ' active'
    else:
        return ''
