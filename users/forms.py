from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


# When looking to add or take away specific fields from a form you must create a new form class that inherits from
# the original form you wish to edit.
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        # We need the class Meta to discern which model this form interacts with and to nail down the order in which our
        # fields appear in our form.
        model = User

        # Note that password 1&2 are the password and confirmation fields
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']