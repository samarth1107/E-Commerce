from django import forms
from django.forms import ModelForm
from core.models import profile,product_category,products
from django.contrib.auth.forms import UserCreationForm

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


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    file= forms.FileField(widget=forms.FileInput(attrs={"class": "form-control"}))

    class Meta:
        model = profile
        fields = ('username', 'email', 'password1', 'password2', 'is_seller','file')

class ProductForm(ModelForm):
    class Meta:
        model=products
        fields=['Product_title','Brand','Product_mrp','Selling_price','category_id','Product_description','Quantity_available','Country_of_origin','Product_image','Product_image_2']