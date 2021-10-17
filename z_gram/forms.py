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

    class UpdateUserProfileForm(forms.ModelForm):
        class Meta:
            model = UserProfile
            fields = ['username', 'location', 'profile_picture', 'bio']

    class UpdateUserForm(forms.ModelForm):
        email = forms.EmailField(max_length=120, help_text='Required. enter a valid email address.')

        class Meta:
            model = User
            fields = ('username', 'email')
