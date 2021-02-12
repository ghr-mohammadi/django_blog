from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Category, Tag


# @login_required
def home(request):
    messages.success(request, 'متن نمایشی جهت تست')
    messages.info(request, 'متن نمایشی جهت تست')
    categories = Category.objects.filter(parent=None)
    tags = Tag.objects.all()
    return render(request, 'blog/home.html', {'categories': categories, 'tags': tags})


def category(request, name):
    parent = get_object_or_404(Category, name=name) if name != 'None' else None
    categories = Category.objects.filter(parent=parent)
    tags = Tag.objects.all()
    return render(request, 'blog/category.html', {'parent': parent, 'categories': categories, 'tags': tags})
