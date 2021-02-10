from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from blog.models import BlogUser
from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            blog_user = BlogUser.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone_number=form.cleaned_data['phone_number'])
            blog_user.save()
            blog_user.groups.add(Group.objects.get(name='ساده'))
            login(request=request, user=blog_user)
            return HttpResponseRedirect(reverse('blog:index'))
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
