from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile, Subprofile
from django.core.exceptions import ValidationError

class RegisterUser(UserCreationForm):
    
    image = forms.ImageField(label='Imagen de Perfil', required=False, widget=forms.FileInput(attrs={'class' : ''}))
    username = forms.CharField(max_length=30,label='Nombre de Usuario', required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario','class' : ''}))
    email = forms.EmailField(max_length=254,label='Correo Electrónico',required=True, widget=forms.EmailInput(attrs={'placeholder': 'Correo Electrónico','class' : ''}))
    password1 = forms.CharField(max_length=30,label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña','class' : ''}))
    password2 = forms.CharField(max_length=30,label='Confirmacion de Contraseña', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña','class' : ''}))
    class Meta: 
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya está registrado.')
        return email
    
    def create_profile(self,user):
        image = self.cleaned_data['image']
        if image == None:
            image = 'default.jpg'
        Profile.objects.create(user=user,image=image)
    

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

class EditUserForm(forms.ModelForm):
    username = forms.CharField(max_length=30,label='Nombre de Usuario', required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario','class' : ''}))
    email = forms.EmailField(max_length=254,label='Correo Electrónico',required=True, widget=forms.EmailInput(attrs={'placeholder': 'Correo Electrónico','class' : ''}))
    class Meta:
        model = User
        fields = ['username', 'email']
        
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está registrado.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya está registrado.')
        return email
    
class RegisterSubuser(forms.ModelForm):
    username = forms.CharField(
        max_length=30,label='Nombre de Usuario',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario','class' : ''}))
    
    email = forms.EmailField(
        max_length=254,
        label='Correo Electrónico',
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Correo Electrónico','class' : ''}))
    
    password1 = forms.CharField(
        max_length=30,
        label='Contraseña',
        required=True, 
        error_messages={
            'Too short' : 'La contraseña debe tener al menos 8 caracteres.',
            'isnumeric' : 'La contraseña no debe ser un número.'},
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña','class' : ''}))
    password2 = forms.CharField(
        max_length=30,
        label='Confirmacion de Contraseña',
        required=True, 
        error_messages={
            'password mismatch' : 'Las contraseñas no coinciden.',
        },
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña','class' : ''}))
    image = forms.ImageField(
        label='Imagen de Perfil',
        required=False, 
        widget=forms.FileInput(attrs={'class' : ''}))
    
    class Meta:
        model = Subprofile
        fields = ['username', 'email', 'password1', 'password2', 'image']

    def __init__(self,request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        
    def create_subprofile(self):
        image = self.cleaned_data.get('image','default.jpg')
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password1 = self.cleaned_data['password1']
        profile = Profile.objects.get(user=self.request.user)
        Subprofile.objects.create(username = username,email = email,password= password1,image=image,profile_id=profile)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        profile = Profile.objects.get(user = self.request.user)
        if Subprofile.objects.filter(profile_id = profile, username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está registrado.')
        if len(username) < 8:
            raise forms.ValidationError('El nombre de usuario debe tener al menos 8 caracteres.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if Subprofile.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya está registrado.')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            error = ValidationError(self.fields['password2'].error_messages['password mismatch'], 
                                    code='password mismatch')
            self.add_error('password2', error)
        if len(password1) < 8:
            error = ValidationError(self.fields['password1'].error_messages['Too short'], 
                                    code='Too short')
            self.add_error('password1', error)
        if password1.isdigit():
            error = ValidationError(self.fields['password1'].error_messages['isnumeric'], 
                                    code='isnumeric')
            self.add_error('password1', error)
        return password1,password2
    
    
    