from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile
from django.forms import ModelForm
from payment.models import ShippingAddress


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'mobile', 'email', 'password1', 'password2']


class User_form(ModelForm):
    class Meta:
        model = Profile
        fields = ["address"]
