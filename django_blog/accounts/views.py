from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from blog.models import BlogUser
from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            blog_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            blog_user.groups.add(Group.objects.get(name='ساده'))
            login(request=request, user=blog_user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
