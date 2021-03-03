from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
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
            messages.success(request, "حساب کاربری با موفقیت ایجاد شد.")
            return HttpResponseRedirect(reverse('blog:home'))
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def delete(request):
    try:
        user = request.user
        user.delete()
        messages.success(request, "حساب کاربری با موفقیت حذف شد.")
    except:
        messages.error(request, "حذف حساب کاربری با خطا موافق شد.")

    return HttpResponseRedirect(reverse('blog:home'))
