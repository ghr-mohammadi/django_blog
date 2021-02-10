from django.contrib.auth.forms import UserCreationForm
from blog.models import BlogUser


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['phone_number'].required = True

    class Meta:
        model = BlogUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'username']
