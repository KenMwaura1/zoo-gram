from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from z_gram.models import UserProfile, UserPost, UserComment


class RegisterForm(UserCreationForm):
    """
    user registration form that inherits UserCreationForm allowing us to have builtin fields, password validation
    and methods like setting password
    """
    email = forms.EmailField(max_length=120, help_text='Required. Enter a valid email address')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

