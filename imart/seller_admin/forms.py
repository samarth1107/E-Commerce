from django import forms
from core.models import profile
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    captcha = CaptchaField()
