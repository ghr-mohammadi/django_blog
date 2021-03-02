from django import forms
from .models import Comment, Post, BlogUser


class SimpleCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'title', 'text', 'category', 'tags', 'is_activated']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'is_activated']


class BlogUserForm(forms.ModelForm):
    class Meta:
        model = BlogUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'image']
