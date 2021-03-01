from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.core.paginator import Paginator
from django.db.models.expressions import RawSQL
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from .forms import SimpleCommentForm, PostForm, CommentForm
from .models import Category, Tag, Post, Comment, BlogUser


def home(request):
    categories = Category.objects.filter(parent=None)
    tags = Tag.objects.all()
    posts = Post.objects.filter(is_accepted=True, is_activated=True)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    return render(request, 'blog/home.html', {'categories': categories, 'tags': tags, 'posts': page_posts})


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


@require_http_methods(["GET", "POST"])
def post(request, id):
    post = get_object_or_404(Post, id=id)
    if not post.is_accepted or not post.is_activated:
        return HttpResponseForbidden()
    form = SimpleCommentForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'برای ثبت کامنت باید با حساب کاربری وارد شوید.')
            return HttpResponseRedirect(reverse('blog:post', args=[id]))
        form = SimpleCommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(creator=request.user, text=form.cleaned_data['text'], is_activated=True, post=post)
            messages.success(request, 'کامنت شما با موفقیت ثبت شد. پس از تایید نهایی کامنت شما در سایت قرار می‌گیرد.')
            return HttpResponseRedirect(reverse('blog:post', args=[id]))
    parent = post.category.parent
    categories = Category.objects.filter(parent=parent)
    tags = Tag.objects.all()
    comments = Comment.objects.filter(is_accepted=True, is_activated=True, post=post)
    context = {
        'parent': parent,
        'categories': categories,
        'tags': tags,
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'blog/post.html', context)


def posts_of(request, username):
    blog_user = get_object_or_404(BlogUser, username=username)
    categories = Category.objects.filter(parent=None)
    tags = Tag.objects.all()
    posts = Post.objects.filter(is_accepted=True, is_activated=True, creator=blog_user)
    return render(request, 'blog/posts_of.html', {'categories': categories, 'tags': tags, 'posts': posts})


@login_required
def my_works(request):
    blog_user = request.user
    categories = Category.objects.filter(parent=None)
    tags = Tag.objects.all()
    posts = Post.objects.filter(creator=blog_user)
    comments = Comment.objects.filter(creator=blog_user)
    return render(request, 'blog/my_works.html', {'categories': categories, 'tags': tags, 'posts': posts, 'comments': comments})


@require_http_methods(["GET", "POST"])
@permission_required('blog.add_post')
def create_post(request):
    blog_user = request.user
    categories = Category.objects.filter(parent=None)
    tags = Tag.objects.all()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = blog_user
            post.save()
            form.save_m2m()
            messages.success(request, 'پست شما با موفقیت ثبت شد و پس از تایید نهایی برای نمایش عمومی در سایت قرار می‌گیرد.')
            return HttpResponseRedirect(reverse('blog:create_post'))
    messages.info(request, 'شما می‌تواند با استفاده از فرم زیر پست خود را منتشر کنید.')
    return render(request, 'blog/create_post.html', {'categories': categories, 'tags': tags, 'form': form})


@require_http_methods(["GET", "POST"])
@permission_required('blog.change_post')
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    blog_user = request.user
    if post.creator != blog_user:
        messages.warning(request, 'شما امکان اصلاح پست در خواست شده را ندارید.')
        return HttpResponseRedirect(reverse('blog:my_works'))
    categories = Category.objects.filter(parent=None)
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post.image = form.cleaned_data['image'] if form.cleaned_data['image'] else None
            post.title = form.cleaned_data['title']
            post.text = form.cleaned_data['text']
            post.category = form.cleaned_data['category']
            post.tags.set(form.cleaned_data['tags'])
            post.is_activated = form.cleaned_data['is_activated']
            post.is_accepted = False
            post.save()
            messages.success(request, 'پست شما با موفقیت اصلاح شد و پس از تایید نهایی برای نمایش عمومی در سایت قرار می‌گیرد.')
            return HttpResponseRedirect(reverse('blog:my_works'))
        else:
            return render(request, 'blog/edit_post.html', {'categories': categories, 'tags': tags, 'form': form})
    else:
        messages.info(request, 'شما می‌تواند با استفاده از فرم زیر پست خود را اصلاح کنید.')
        init_val = {
            'image': post.image,
            'title': post.title,
            'text': post.text,
            'category': post.category,
            'tags': Tag.objects.filter(post=post),
            'is_activated': post.is_activated
        }
        form = PostForm(initial=init_val)
        return render(request, 'blog/edit_post.html', {'categories': categories, 'tags': tags, 'form': form})


@permission_required('blog.delete_post')
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    blog_user = request.user
    if post.creator != blog_user:
        messages.error(request, 'شما امکان حذف پست در خواست شده را ندارید.')
        return HttpResponseRedirect(reverse('blog:my_works'))
    post.delete()
    messages.success(request, 'پست در خواست شده با موفقیت حذف شد.')
    return HttpResponseRedirect(reverse('blog:my_works'))


@require_http_methods(["GET", "POST"])
@permission_required('blog.change_comment')
def edit_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    blog_user = request.user
    if comment.creator != blog_user:
        messages.warning(request, 'شما امکان اصلاح کامنت در خواست شده را ندارید.')
        return HttpResponseRedirect(reverse('blog:my_works'))
    categories = Category.objects.filter(parent=None)
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.text = form.cleaned_data['text']
            comment.is_activated = form.cleaned_data['is_activated']
            comment.is_accepted = False
            comment.save()
            messages.success(request, 'کامنت شما با موفقیت اصلاح شد و پس از تایید نهایی برای نمایش عمومی در سایت قرار می‌گیرد.')
            return HttpResponseRedirect(reverse('blog:my_works'))
        else:
            return render(request, 'blog/edit_post.html', {'categories': categories, 'tags': tags, 'form': form})
    else:
        messages.info(request, 'شما می‌تواند با استفاده از فرم زیر کامنت خود را اصلاح کنید.')
        init_val = {
            'text': comment.text,
            'is_activated': comment.is_activated
        }
        form = CommentForm(initial=init_val)
        return render(request, 'blog/edit_post.html', {'categories': categories, 'tags': tags, 'form': form})


@permission_required('blog.delete_comment')
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    blog_user = request.user
    if comment.creator != blog_user:
        messages.error(request, 'شما امکان حذف کامنت در خواست شده را ندارید.')
        return HttpResponseRedirect(reverse('blog:my_works'))
    comment.delete()
    messages.success(request, 'کامنت در خواست شده با موفقیت حذف شد.')
    return HttpResponseRedirect(reverse('blog:my_works'))


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
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    return render(request, 'blog/bests.html', {'categories': categories, 'tags': tags, 'posts': page_posts})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:home'))
