from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models.expressions import RawSQL
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Category, Tag, Post, Comment, BlogUser


def home(request):
    categories = Category.objects.filter(parent=None)
    tags = Tag.objects.all()
    posts = Post.objects.filter(is_accepted=True, is_activated=True)
    return render(request, 'blog/home.html', {'categories': categories, 'tags': tags, 'posts': posts})


def category(request, name):
    parent = get_object_or_404(Category, name=name) if name != 'None' else None
    categories = Category.objects.filter(parent=parent)
    tags = Tag.objects.all()

    def get_branch(parent):
        deeper = Category.objects.none()
        for par in list(parent):
            parent |= Category.objects.filter(parent=par)
        deeper |= parent
        for par in parent:
            deeper |= Category.objects.filter(parent=par)
        return get_branch(parent) if deeper.difference(parent) else parent

    if parent:
        branch = get_branch(Category.objects.filter(name=parent.name))
    else:
        branch = Category.objects.all()

    posts = Post.objects.none()
    for category in branch:
        posts |= Post.objects.filter(is_accepted=True, is_activated=True, category=category)

    return render(request, 'blog/category.html', {'parent': parent, 'categories': categories, 'tags': tags, 'posts': posts})


def categories(request):
    categories = Category.objects.filter(parent=None)
    tags = Tag.objects.all()
    posts = Post.objects.filter(is_accepted=True, is_activated=True)
    return render(request, 'blog/categories.html', {'categories': categories, 'tags': tags, 'posts': posts})


def tag(request, name):
    specific_tag = get_object_or_404(Tag, name=name)
    categories = Category.objects.filter(parent=None)
    tags = Tag.objects.all()
    posts = Post.objects.filter(is_accepted=True, is_activated=True, tags=specific_tag)
    return render(request, 'blog/tag.html', {'categories': categories, 'tags': tags, 'posts': posts, 'specific_tag': specific_tag})


def tags(request):
    tags = Tag.objects.all()
    posts = Post.objects.filter(is_accepted=True, is_activated=True)
    return render(request, 'blog/tags.html', {'tags': tags, 'posts': posts})


def post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.is_accepted and post.is_activated:
        parent = post.category.parent
        categories = Category.objects.filter(parent=parent)
        tags = Tag.objects.all()
        comments = Comment.objects.filter(post=post)
        return render(request, 'blog/post.html', {'parent': parent, 'categories': categories, 'tags': tags, 'post': post, 'comments': comments})
    else:
        return HttpResponseForbidden()


def posts_of(request, username):
    blog_user = get_object_or_404(BlogUser, username=username)
    categories = Category.objects.filter(parent=None)
    tags = Tag.objects.all()
    posts = Post.objects.filter(is_accepted=True, is_activated=True, creator=blog_user)
    return render(request, 'blog/posts_of.html', {'categories': categories, 'tags': tags, 'posts': posts})


def search(request):
    name = '%' + request.GET.get('input') + '%'
    categories = Category.objects.raw('select * from blog_category where name ilike %s;', [name])
    tags = Tag.objects.raw('select * from blog_tag where name ilike %s;', [name])
    posts = Post.objects.raw('select * from blog_post where text ilike %s or title ilike %s;', [name, name])
    return render(request, 'blog/search.html', {'categories': categories, 'tags': tags, 'posts': posts})


def bests(request):
    categories = Category.objects.filter(parent=None)
    tags = Tag.objects.all()
    posts = Post.objects.filter(is_accepted=True, is_activated=True).order_by('-like_qty', 'dislike_qty')
    return render(request, 'blog/bests.html', {'categories': categories, 'tags': tags, 'posts': posts})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:home'))
