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
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Hasło'}),
                               label='password', max_length=128)
    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Powtórz hasło'}),
                               label='password_confirmation', max_length=128)


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Hasło'}),
                               label='password', max_length=128)


APROVING_CHOICES = (
        (1, "tak"),
        (2, "nie"),
)


class AprovingForm(forms.Form):
    choice = forms.ChoiceField(choices=APROVING_CHOICES, initial=1, label="Potwierdź")


class ChangeUserDetailsForm(forms.Form):
    first_name = forms.CharField(label='Imię',
                                 widget=forms.TextInput(attrs={'placeholder': 'Imię'}),
                                 max_length=150)
    last_name = forms.CharField(label='Nazwisko',
                                widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
                                max_length=150)
    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'placeholder': 'Email'}))


class ChangeUserPasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Podaj aktualne hasło'}),
                                   label='password', max_length=128)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Podaj nowe hasło'}),
                                   label='password', max_length=128)
    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'Powtórz nowe hasło'}),
                                            label='password_confirmation', max_length=128)
