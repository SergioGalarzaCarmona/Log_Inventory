from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterUser(UserCreationForm):
    
    image = forms.ImageField(label='Imagen de Perfil', required=False, widget=forms.FileInput(attrs={'class' : ''}))
    username = forms.CharField(max_length=30,label='Nombre de Usuario', required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario','class' : ''}))
    email = forms.EmailField(max_length=254,label='Correo Electrónico', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Correo Electrónico','class' : ''}))
    password1 = forms.CharField(max_length=30,label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña','class' : ''}))
    password2 = forms.CharField(max_length=30,label='Confirmacion de Contraseña', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña','class' : ''}))
    class Meta: 
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}

class LoginUser(forms.Form):
    username = forms.CharField(max_length=30,label='Nombre de Usuario', required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario','class' : ''}))
    password = forms.CharField(max_length=30,label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña','class' : ''}))
    
    class Meta:
        model = User
        fields = ['username', 'password']
        help_texts = {k:"" for k in fields}