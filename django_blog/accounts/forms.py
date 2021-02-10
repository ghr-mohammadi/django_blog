from django import forms
from blog.models import BlogUser


class SignUpForm(forms.ModelForm):
    password = forms.CharField(label="گذرواژه", widget=forms.PasswordInput)
    password_again = forms.CharField(label="تکرار گذرواژه", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['phone_number'].required = True

    class Meta:
        model = BlogUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'username']

    def clean_password_again(self):
        password = self.cleaned_data.get("password").strip()
        password_again = self.cleaned_data.get("password_again").strip()
        if not (password or password_again):
            raise ValidationError('گذرواژه نامناسب!')
        if password != password_again:
            raise ValidationError('عدم تطابق گذرواژه!')
        return password_again
