from django import forms

from .models import CustomUser

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class Login(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class Registration(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'avatar', 'password1', 'password2']