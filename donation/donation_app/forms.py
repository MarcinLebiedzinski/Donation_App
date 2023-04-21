from django import forms
from .models import Category, Institution, Donation
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='Imię',
                                 widget=forms.TextInput(attrs={'placeholder': 'Imię'}),
                                 max_length=150)
    last_name = forms.CharField(label='Nazwisko',
                                widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
                                max_length=150)
    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='Hasło',
                               widget=forms.TextInput(attrs={'placeholder': 'Hasło'}),
                               max_length=128)
    password_confirmation = forms.CharField(label='Powtórz hasło',
                                            widget=forms.TextInput(attrs={'placeholder': 'Powtórz hasło'}),
                                            max_length=128)

