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


class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'image']


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


class UpdatePharmacyForm(ModelForm):
    class Meta:
        model = Pharmacy
        fields = '__all__'
        exclude = ['user', 'date_created']


class UpdateOrder(ModelForm):
    class Meta:
        model = Order
        fields = ['delivary_status']
