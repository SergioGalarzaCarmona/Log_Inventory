from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, PasswordResetForm, SetPasswordForm
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

class LoginUser(AuthenticationForm):
    username = forms.CharField(max_length=30,label='Nombre de Usuario', required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario','class' : ''}))
    password = forms.CharField(max_length=30,label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña','class' : ''}))
    
    class Meta:
        model = User
        fields = ['username', 'password']
        
class PasswordReset(PasswordResetForm):
    email = forms.EmailField(max_length=254,label='Correo Electrónico', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Correo Electrónico','class' : ''}))
    
    class Meta:
        fields = ['email']
        
class SetPassword(SetPasswordForm):
    new_password1 = forms.CharField(max_length=30,label='Nueva contraseña', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña','class' : ''}))
    new_password2 = forms.CharField(max_length=30,label='Confirmación de  nueva contraseña', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña','class' : ''}))
    
    class Meta:
        fields = ['new_password1', 'new_password2']