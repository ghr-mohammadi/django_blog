from django import forms
from .models import Comment


class SimpleCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
