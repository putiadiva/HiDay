from cProfile import label
from django import forms
from django.db import connection

# login
# register pengguna
# register a

class LoginForm(forms.Form):
    email = forms.CharField(
        label=("Email"), required=True, max_length=50)
    password = forms.CharField(
        label=("Password"), widget=forms.PasswordInput, required=True, max_length=25)


class RegisterPenggunaForm(forms.Form):
    email = forms.CharField(
        label=("Email"), required=True, max_length=50)
    password = forms.CharField(
        label=("Password"), widget=forms.PasswordInput, required=True, max_length=25)
    nama_area = forms.CharField(
        label=("Nama_area"), required=True, max_length=25)

    
class RegisterAdminForm(forms.Form):
    email = forms.CharField(
        label=("Email"), required=True, max_length=50)
    password = forms.CharField(
        label=("Password"), widget=forms.PasswordInput, required=True, max_length=25)
