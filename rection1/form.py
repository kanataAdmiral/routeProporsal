from django import forms
from .models import User


class LoginForm(forms.Form):
    id = forms.CharField(label='id:', max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'
