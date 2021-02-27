from django import forms
from .models import Comment, Post


class SimpleCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'title', 'text', 'category', 'tags', 'is_activated']
