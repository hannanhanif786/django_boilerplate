from django.forms import ModelForm
from django import forms
from .models import MyUser
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from django.contrib.auth import get_user_model


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        exclude = ["image"]


User = get_user_model()


class RegisterForm(UserCreationForm):

    # password = forms.CharField(widget=forms.PasswordInput)
    # password_2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email"]


class ChangePassword(forms.Form):
    oldpasssword = forms.CharField(max_length=20, widget=forms.PasswordInput)
    newpasssword = forms.CharField(max_length=20, widget=forms.PasswordInput)
    confirm_newpasssword = forms.CharField(max_length=20, widget=forms.PasswordInput)
