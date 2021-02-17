from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Category, Tag, Post


def home(request):
    messages.success(request, 'متن نمایشی جهت تست')
    messages.info(request, 'متن نمایشی جهت تست')
    categories = Category.objects.filter(parent=None)
    tags = Tag.objects.all()
    posts = Post.objects.filter(is_accepted=True, is_activated=True)
    return render(request, 'blog/home.html', {'categories': categories, 'tags': tags, 'posts': posts})


def category(request, name):
    parent = get_object_or_404(Category, name=name) if name != 'None' else None
    categories = Category.objects.filter(parent=parent)
    tags = Tag.objects.all()

    def get_branch(parent):
        none = Category.objects.none()
        plist = list(parent)
        for par in plist:
            parent |= Category.objects.filter(parent=par)
        none |= parent
        for par in parent:
            none |= Category.objects.filter(parent=par)
        if set(none) - set(parent):
            return get_branch(parent)
        else:
            return parent

    if parent:
        branch = get_branch(Category.objects.filter(name=parent.name))
    else:
        branch = Category.objects.all()

    posts = Post.objects.none()
    for category in branch:
        posts |= Post.objects.filter(is_accepted=True, is_activated=True, category=category)

    return render(request, 'blog/category.html', {'parent': parent, 'categories': categories, 'tags': tags, 'posts': posts})


def tag(request, name):
    specific_tag = get_object_or_404(Tag, name=name)
    categories = Category.objects.filter(parent=None)
    tags = Tag.objects.all()
    posts = Post.objects.filter(is_accepted=True, is_activated=True, tags=specific_tag)
    return render(request, 'blog/tag.html', {'categories': categories, 'tags': tags, 'posts': posts, 'specific_tag': specific_tag})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:home'))
