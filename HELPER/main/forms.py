from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . import models

class CryptoForm(forms.ModelForm):

    class Meta:
        model = models.Crypto
        fields = ['name', 'ticker', 'amount']


class ShareForm(forms.ModelForm):

    class Meta:
        model = models.Share
        fields = ['name', 'ticker', 'amount']


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

