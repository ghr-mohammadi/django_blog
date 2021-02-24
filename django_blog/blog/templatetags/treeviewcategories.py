from django import template
from blog.models import Category

register = template.Library()


@register.filter
def has_childs(category):
    if Category.objects.filter(parent=category):
        return True
    return False


@register.filter
def all_childs(category):
    return Category.objects.filter(parent=category)
