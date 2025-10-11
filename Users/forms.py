from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from django import forms
from .models import Profile, Subprofile, SubprofilesGroup, PermissionsGroup
from django.core.exceptions import ValidationError


# Forms to register users and subusers
class RegisterUser(UserCreationForm):

    image = forms.ImageField(
        label="Imagen de Perfil",
        required=False,
        widget=forms.FileInput(attrs={"class": ""}),
    )
    username = forms.CharField(
        max_length=30,
        label="Nombre de Usuario",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Nombre de Usuario", "class" : "restricted",}),
    )
    email = forms.EmailField(
        max_length=254,
        label="Correo Electrónico",
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "Correo Electrónico", "class": ""}
        ),
    )
    password1 = forms.CharField(
        max_length=30,
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña", "class": ""}),
    )
    password2 = forms.CharField(
        max_length=30,
        label="Confirmacion de Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirmar Contraseña", "class": ""}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        help_texts = {k: "" for k in fields}

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya está registrado.")
        if len(username) < 8:
            raise forms.ValidationError(
                "El nombre de usuario debe tener al menos 8 caracteres."
            )
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ya está registrado.")
        return email

    def create_profile(self, user, image=None):
        if image == None:
            image = "default.jpg"
        Profile.objects.create(user=user, image=image)


class RegisterSubprofileGroup(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        label="Nombre del grupo",
        widget=forms.TextInput(attrs={"placeholder": "Nombre del Grupo", "class": ""}),
        error_messages={
            "is_too_short": "El nombre del grupo debe tener al menos 8 caracteres.",
            "unique": "El nombre del grupo ya está registrado.",
            "invalid": "El nombre del grupo no puede ser el mismo que el del perfil.",
        },
    )
    permissions = forms.ModelChoiceField(
        queryset=PermissionsGroup.objects.all(),
        required=True,
        label="Tipo de usuario",
        widget=forms.Select(attrs={"class": ""}),
    )
    image = forms.ImageField(
        required=False,
        label="imagen",
        widget=forms.FileInput(attrs={"class": "", "id": "image_group"}),
    )

    description = forms.CharField(
        max_length=1000,
        label="Descripción",
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": "Descripcion del grupo", "class": ""}
        ),
    )

    class Meta:
        model = SubprofilesGroup
        fields = ["name", "image"]

    def __init__(self, *args, **kwargs):
        user_pk = kwargs.pop("user_pk", None)
        self.user_pk = user_pk
        super().__init__(*args, **kwargs)

    def create_subprofile_group(self, image="default_group.jpg"):
        name = self.cleaned_data["name"]
        permissions_group = self.cleaned_data["permissions"]
        description = self.cleaned_data["description"]
        user = User.objects.get(pk=self.user_pk)
        profile = Profile.objects.get(user=user)

        return SubprofilesGroup.objects.create(
            profile=profile,
            name=name,
            image=image,
            permissions=permissions_group,
            description=description,
        )

    def clean_name(self):
        name = self.cleaned_data["name"]
        user = User.objects.get(pk=self.user_pk)
        profile = Profile.objects.get(user=user)
        if SubprofilesGroup.objects.filter(profile=profile, name=name).exists():
            error = ValidationError(
                self.fields["name"].error_messages["unique"], code="unique"
            )
            self.add_error("name", error)
        if len(name) < 8:
            error = ValidationError(
                self.fields["name"].error_messages["is_too_short"], code="is_too_short"
            )
            self.add_error("name", error)
        return name


class RegisterSubuser(UserCreationForm):

    group = forms.ModelChoiceField(
        queryset=None,
        label="Grupo",
        required=True,
        widget=forms.Select(attrs={"class": ""}),
    )
    email = forms.EmailField(
        max_length=254,
        label="Correo Electrónico",
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "Correo Electrónico", "class": ""}
        ),
        error_messages={
            'invalid_email' : 'El email ya está registrado.'
        }
    )

    password1 = forms.CharField(
        max_length=30,
        label="Contraseña",
        required=True,
        error_messages={
            "Too short": "La contraseña debe tener al menos 8 caracteres.",
            "isnumeric": "La contraseña no debe ser un número.",
        },
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña", "class": ""}),
    )
    password2 = forms.CharField(
        max_length=30,
        label="Confirmacion de Contraseña",
        required=True,
        error_messages={
            "password mismatch": "Las contraseñas no coinciden.",
        },
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirmar Contraseña", "class": ""}
        ),
    )
    image = forms.ImageField(
        label="Imagen de Perfil",
        required=False,
        widget=forms.FileInput(attrs={"class": ""}),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2", "group"]
        help_texts = {k: "" for k in fields}

    def __init__(self, *args, **kwargs):
        user_pk = kwargs.pop("user_pk", None)
        self.user_pk = user_pk
        super().__init__(*args, **kwargs)
        if user_pk:
            user = User.objects.get(pk=user_pk)
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                profile = None
            self.fields["group"].queryset = SubprofilesGroup.objects.filter(
                profile=profile, is_active=True
            )
        self.fields["first_name"].required = True
        self.fields["first_name"].widget.attrs = {
            "placeholder": "Nombre",
            "class" : "restricted",
        }
        self.fields['first_name'].label = "Nombres"
        self.fields["last_name"].required = True
        self.fields["last_name"].widget.attrs = {
            "placeholder": "Apellido",
            "class" : "restricted",
        }
        self.fields['last_name'].label = "Apellidos"

    def create_subprofile(self, user, group_id, image):
        main_user = User.objects.get(pk=self.user_pk)
        profile = Profile.objects.get(user=main_user)
        group = SubprofilesGroup.objects.get(pk=group_id)
        return Subprofile.objects.create(
            user=user, profile=profile, group=group, image=image
        )

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if first_name and last_name:
            exists = Subprofile.objects.filter(
                user__first_name=first_name, user__last_name=last_name
            )

            if exists.exists():
                self.add_error("first_name","Este nombre (nombre y apellido) ya está en uso.")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Subprofile.objects.filter(user__email=email).exists():
            error = ValidationError(
                self.fields["email"].error_messages["invalid_email"],
                code="invalid_email",
            )
            self.add_error("email", error)
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            error = ValidationError(
                self.fields["password2"].error_messages["password mismatch"],
                code="password mismatch",
            )
            self.add_error("password2", error)
        if len(password1) < 8:
            error = ValidationError(
                self.fields["password1"].error_messages["Too short"], code="Too short"
            )
            self.add_error("password1", error)
        if password1.isdigit():
            error = ValidationError(
                self.fields["password1"].error_messages["isnumeric"], code="isnumeric"
            )
            self.add_error("password1", error)
        return password2


# Form to login
class LoginUser(AuthenticationForm):
    username = forms.CharField(
        max_length=30,
        label="Nombre de Usuario",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nombre de Usuario",
                "class": "",
                "id": "username_login_id",
            }
        ),
    )
    password = forms.CharField(
        max_length=30,
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña", "class": ""}),
    )

    class Meta:
        model = User
        fields = ["username", "password"]


# Forms to reset and set password
class PasswordReset(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        label="Correo Electrónico",
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "Correo Electrónico", "class": ""}
        ),
    )

    class Meta:
        fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("El email no está registrado.")
        return email


class SetPassword(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=30,
        label="Nueva contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña", "class": ""}),
    )
    new_password2 = forms.CharField(
        max_length=30,
        label="Confirmación de  nueva contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirmar Contraseña", "class": ""}
        ),
    )

    class Meta:
        fields = ["new_password1", "new_password2"]


# Forms to edit the user's or subuser's profile
class EditUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30,
        label="Nombre de Usuario",
        required=True,
        error_messages={
            "unique": "El nombre de usuario ya está registrado.",
            "is_too_short": "El nombre de usuario debe tener al menos 8 caracteres.",
            "invalid": "La contraseña no coincide.",
        },
        widget=forms.TextInput(attrs={"placeholder": "Nombre de Usuario", "class" : "restricted",}),
    )
    email = forms.EmailField(
        max_length=254,
        label="Correo Electrónico",
        required=True,
        error_messages={"unique": "El email ya está registrado."},
        widget=forms.EmailInput(
            attrs={"placeholder": "Correo Electrónico", "class": ""}
        ),
    )
    password = forms.CharField(
        max_length=30,
        label="Contraseña",
        required=True,
        error_messages={"invalid": "La contraseña no coincide."},
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña", "class": ""}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def __init__(self, *args, **kwargs):
        if "user_pk" in kwargs:
            user_pk = kwargs.pop("user_pk")
            self.user_pk = user_pk
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]
        users = User.objects.filter(username=username).exclude(pk=self.user_pk)
        if len(users) > 0:
            error = ValidationError(
                self.fields["username"].error_messages["unique"], code="unique"
            )
            self.add_error("username", error)
        if len(username) < 8:
            error = ValidationError(
                self.fields["username"].error_messages["is_too_short"],
                code="is_too_short",
            )
            self.add_error("username", error)
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        users = User.objects.filter(email=email).exclude(pk=self.user_pk)
        if len(users) > 0:
            error = ValidationError(
                self.fields["email"].error_messages["unique"], code="unique"
            )
            self.add_error("email", error)
        return email

    def clean_password(self):
        password = self.cleaned_data["password"]
        user = User.objects.get(pk=self.user_pk)
        if not user.check_password(password):
            error = ValidationError(
                self.fields["password"].error_messages["invalid"], code="invalid"
            )
            self.add_error("password", error)
        return password


class EditSubprofileForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=254,
        label="Correo Electrónico",
        required=True,
        error_messages={"unique": "El email ya está registrado."},
        widget=forms.EmailInput(
            attrs={"placeholder": "Correo Electrónico", "class": ""}
        ),
    )
    group = forms.ModelChoiceField(
        queryset=None, label="Grupo", widget=forms.Select(attrs={"class": ""})
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "group"]

    def __init__(self, *args, **kwargs):
        user_pk = kwargs.pop("user_pk")
        self.user_pk = user_pk
        permissions = kwargs.pop("permissions")
        self.permissions = permissions
        super().__init__(*args, **kwargs)
        self.fields["group"].queryset = SubprofilesGroup.objects.filter(
            profile=self.instance.subprofile.profile
        )
        self.fields["group"].initial = self.instance.subprofile.group
        if permissions != "admin":
            self.fields["group"].disabled = True
        self.fields["first_name"].required = True
        self.fields["first_name"].widget.attrs = {
            "placeholder": "Nombre",
            "class" : "restricted",
        }
        self.fields['first_name'].label = "Nombres"
        self.fields["last_name"].required = True
        self.fields["last_name"].widget.attrs = {
            "placeholder": "Apellido",
            "class" : "restricted",
        }
        self.fields['last_name'].label = "Apellidos"

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if first_name and last_name:
            exists = Subprofile.objects.filter(
                user__first_name=first_name, user__last_name=last_name
            )

            # exclude current instance when editing
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.subprofile.pk)

            if exists.exists():
                self.add_error("first_name", "Este nombre (nombre y apellido) ya está en uso.")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data["email"]
        users = User.objects.filter(email=email).exclude(pk=self.user_pk)
        if len(users) > 0:
            error = ValidationError(
                self.fields["email"].error_messages["unique"], code="unique"
            )
            self.add_error("email", error)
        return email


class EditSubprofileGroupForm(forms.ModelForm):
    name = forms.CharField(
        max_length=24,
        required=True,
        label="Nombre del grupo:",
        widget=forms.TextInput(),
        error_messages={
            "is_too_short": "El nombre del grupo debe tener al menos 8 caracteres.",
            "unique": "El nombre del grupo ya está registrado.",
            "invalid": "El nombre del grupo no puede ser el mismo que el del perfil.",
        },
    )

    permissions = forms.ModelChoiceField(
        queryset=PermissionsGroup.objects.all(),
        required=True,
        label="Tipo de grupo:",
        widget=forms.Select(),
    )

    description = forms.CharField(
        max_length=1000, label="Descripción", required=False, widget=forms.Textarea()
    )

    def __init__(self, *args, **kwargs):
        user_pk = kwargs.pop("user_pk", None)
        self.user_pk = user_pk
        super().__init__(*args, **kwargs)
        self.fields["permissions"].initial = self.instance.permissions
        self.fields["name"].widget.attrs = {
            "id": f"id_name_{self.instance.pk}",
            "placeholder": "Nombre del Grupo",
        }
        self.fields["permissions"].widget.attrs = {
            "id": f"id_permissions_{self.instance.pk}",
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        profile = Profile.objects.get(user_id=self.user_pk)
        subgroup = SubprofilesGroup.objects.filter(name=name, profile=profile).exclude(
            pk=self.instance.pk
        )
        if subgroup.exists():
            error = ValidationError(
                self.fields["name"].error_messages["unique"], code="Unique"
            )
            self.add_error("name", error)
        if len(name) < 8:
            error = ValidationError(
                self.fields["name"].error_messages["is_too_short"], code="is_too_short"
            )
            self.add_error("name", error)
        if name == profile.user.username:
            error = ValidationError(
                self.fields["name"].error_messages["invalid"], code="invalid"
            )
            self.add_error("name", error)
        return name

    class Meta:
        model = SubprofilesGroup
        fields = ["name", "permissions", "description"]


class SetImageForm(forms.Form):
    image = forms.ImageField(
        label="Imagen de Perfil",
        required=True,
        widget=forms.FileInput(attrs={"class": ""}),
    )

    class Meta:
        fields = ["image"]
