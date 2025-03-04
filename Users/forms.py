from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile, Subprofile, SubprofilesGroup, PermissionsGroup
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

class RegisterUser(UserCreationForm):
    
    image = forms.ImageField(
        label='Imagen de Perfil', 
        required=False, 
        widget=forms.FileInput(
            attrs={
                'class' : ''
                }
            )
        )
    username = forms.CharField(
        max_length=30,
        label='Nombre de Usuario',
        required=True, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nombre de Usuario',
                'class' : ''
                }
            )
        )
    email = forms.EmailField(
        max_length=254,
        label='Correo Electrónico',
        required=True, 
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Correo Electrónico',
                'class' : ''
                }
            )
        )
    password1 = forms.CharField(
        max_length=30,
        label='Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class' : ''
                }
            )
        )
    password2 = forms.CharField(
        max_length=30,
        label='Confirmacion de Contraseña',
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmar Contraseña',
                'class' : ''
                }
            )
        )
    class Meta: 
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está registrado.')
        if len(username) < 8:
            raise forms.ValidationError('El nombre de usuario debe tener al menos 8 caracteres.')
        return username
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya está registrado.')
        return email
    
    def create_profile(self,user,image = None):
        if image == None:
            image = 'default.jpg'
        Profile.objects.create(user=user,image=image)
    

class LoginUser(AuthenticationForm):
    username = forms.CharField(
        max_length=30,
        label='Nombre de Usuario', 
        required=True, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nombre de Usuario',
                'class' : ''
                }
            )
        )
    password = forms.CharField(
        max_length=30,
        label='Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class' : ''
                }
            )
        )
    
    class Meta:
        model = User
        fields = ['username', 'password']
        
class PasswordReset(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        label='Correo Electrónico', 
        required=True, 
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Correo Electrónico',
                'class' : ''
                }
            )
        )
    
    class Meta:
        fields = ['email']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email no está registrado.')
        return email
        
class SetPassword(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=30,
        label='Nueva contraseña', 
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class' : ''
                }
            )
        )
    new_password2 = forms.CharField(
        max_length=30,
        label='Confirmación de  nueva contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmar Contraseña',
                'class' : ''
                }
            )
        )
    class Meta:
        fields = ['new_password1', 'new_password2']

class EditUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30,
        label='Nombre de Usuario', 
        required=True, 
        error_messages= {
            'unique' : 'El nombre de usuario ya está registrado.',
            'is_too_short': 'El nombre de usuario debe tener al menos 8 caracteres.',
            'invalid': 'La contraseña no coincide.'
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nombre de Usuario',
                'class' : ''
                }
            )
        )
    email = forms.EmailField(
        max_length=254,
        label='Correo Electrónico',
        required=True, 
        error_messages= {
            'unique' : 'El email ya está registrado.'
        },
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Correo Electrónico',
                'class' : ''
                }
            )
        )
    password = forms.CharField(
        max_length=30,
        label='Contraseña',
        required=True, 
        error_messages={
            'invalid': 'La contraseña no coincide.'
        },
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class' : ''
                }
            )
        )
    class Meta:
        model = User
        fields = ['username', 'email', "password"]
    
    def __init__(self, *args, **kwargs):
        if 'user_pk' in kwargs:
            user_pk = kwargs.pop('user_pk')
            self.user_pk = user_pk
        super().__init__(*args, **kwargs)
        
        
    def clean_username(self):
        username = self.cleaned_data['username']
        users = User.objects.filter(username=username).exclude(pk=self.user_pk)
        if len(users) > 0:
            error = ValidationError(self.fields['username'].error_messages['unique'],
                                    code='unique')
            self.add_error('username', error)
        if len(username) < 8:
            error = ValidationError(self.fields['username'].error_messages['is_too_short'], 
                                    code='is_too_short')
            self.add_error('username', error)
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        users = User.objects.filter(email=email).exclude(pk=self.user_pk)
        if len(users) > 0:
            error = ValidationError(self.fields['email'].error_messages['unique'], 
                                    code='unique')
            self.add_error('email', error)
        return email
    
    def clean_password(self):
        password = self.cleaned_data['password']
        user = User.objects.get(pk=self.user_pk)
        if not user.check_password(password):
            error = ValidationError(self.fields['password'].error_messages['invalid'], 
                                    code='invalid')
            self.add_error('password', error)
        return password
    
class SetImageForm(forms.Form):
    image = forms.ImageField(
        label='Imagen de Perfil',
        required=True, 
        widget=forms.FileInput(attrs={'class' : ''})
        )
    class Meta:
        fields = ['image']
        
        
        
    
class RegisterSubuser(UserCreationForm):

    username = forms.CharField(
        max_length=30,
        label='Nombre de Usuario',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario','class' : ''}))
    group = forms.ModelChoiceField (
        queryset=None,
        label='Grupo',
        required=True,
        widget=forms.Select(attrs={'class' : ''}))
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
        model = User
        fields = ['username', 'email', 'password1', 'password2','group']
        help_texts = {k:"" for k in fields}
    
    def __init__(self,*args, **kwargs):
        user_pk = kwargs.pop('user_pk',None)
        self.user_pk = user_pk
        super().__init__(*args, **kwargs)
        if user_pk:
            user = User.objects.get(pk=user_pk)
            profile = Profile.objects.get(user=user)
            self.fields['group'].queryset = SubprofilesGroup.objects.filter(profile=profile) 

    def create_subprofile(self,user, group_id,image):
        main_user = User.objects.get(pk = self.user_pk)
        profile = Profile.objects.get(user = main_user)
        group = SubprofilesGroup.objects.get(pk = group_id)
        return Subprofile.objects.create(user=user,profile=profile,group=group,image=image)
        
    
    def clean_username(self):
        username = self.cleaned_data['username']
        profile = Profile.objects.get(user = self.user_pk)
        if Subprofile.objects.filter(user = self.user_pk, username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está registrado.')
        if len(username) < 8:
            raise forms.ValidationError('El nombre de usuario debe tener al menos 8 caracteres.')
        if username == profile.user.username:
            raise forms.ValidationError('El nombre de usuario no puede ser igual al del perfil.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if Subprofile.objects.filter(email=email).exists() and User.objects.filter(email=email).exists():
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
    
    
class RegisterSubprofileGroup(forms.ModelForm):
    name = forms.CharField(
        max_length=24,
        required = True, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nombre del Grupo',
                'class' : ''
                }
            ),
        error_messages={
            'is_too_short': 'El nombre del grupo debe tener al menos 8 caracteres.',
            'unique' : 'El nombre del grupo ya está registrado.',
            'invalid' : 'El nombre del grupo no puede ser el mismo que el del perfil.'
        }
        )
    image = forms.ImageField(
        required=False,
        widget = forms.FileInput(
            attrs={
                'class' : '',
                'id' : 'image_group'
                }
            )
        )
    class Meta:
        model = SubprofilesGroup
        fields = ['name','image']
        
    def __init__(self, *args, **kwargs):
        user_pk = kwargs.pop('user_pk',None)
        self.user_pk = user_pk
        super().__init__(*args, **kwargs)
        
    def create_subprofile_group(self):
        name = self.cleaned_data['name']
        image = self.cleaned_data.get('image','default_group.jpg')
        user = User.objects.get(pk = self.user_pk)
        profile = Profile.objects.get(user = user)
        permissions = PermissionsGroup.objects.get(pk=1)
        SubprofilesGroup.objects.create(profile=profile,name=name,image=image,permissions=permissions)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        user = User.objects.get(pk = self.user_pk)
        if SubprofilesGroup.objects.filter(user = user, name=name).exists():
            error = ValidationError(self.fields['name'].error_messages['unique'],
                                    code = 'unique')
            self.add_error('name',error)
        if len(name) < 8:
            error = ValidationError(self.fields['name'].error_messages['is_too_short'],
                                    code = 'is_too_short')
            self.add_error('name',error)
        if user.username == name:
            error = ValidationError(self.fields['name'].error_messages['invalid'],
                                    code = 'invalid')
            self.add_error('name',error)
        return name