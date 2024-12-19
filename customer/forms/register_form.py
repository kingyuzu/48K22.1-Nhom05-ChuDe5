from django import forms
from django.contrib.auth.forms import UserCreationForm
from admin_manager.models import User  # Replace with your custom user model

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
