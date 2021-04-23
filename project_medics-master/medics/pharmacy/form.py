from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class CreatePharmacyAdminForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                  'password2', 'first_name', 'last_name']


class CreatePharmacyForm(ModelForm):
    class Meta:
        model = Pharmacy
        fields = ['shop_name', 'phone', 'address', 'area', 'profile_pic']
        widgets = {
            'area': forms.TextInput(attrs={'class': 'required'}),



        }


class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),


        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateCustomerForm(ModelForm):
    class Meta:

        model = Customer
        fields = ['phone', 'profile_pic']


class UpdateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['date_created', 'user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'type': "email"}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'pattern': "[0-9]{11}", 'placeholder': "01316981090"}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),

        }


class UpdatePharmacyForm(ModelForm):
    class Meta:
        model = Pharmacy
        fields = '__all__'
        exclude = ['user', 'date_created']
        widgets = {
            'shop_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'pattern': "[0-9]{11}"}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),

        }


class UpdateOrder(ModelForm):
    class Meta:
        model = Order
        fields = ['delivary_status']
