from django import forms
from .models import Objects, ObjectsGroup
from Users.models import Subprofile
from django.core.exceptions import ValidationError


class ObjectForm(forms.ModelForm):
    name = forms.CharField(
        label="Nombre",
        required=True,
        widget=forms.TextInput(attrs={}),
        error_messages={
            "invalid_lenght": "El nombre es muy corto o muy largo.",
            "unique": "El nombre del objeto solo puede estar resgistrado una sola vez.",
        },
    )

    stock = forms.IntegerField(
        label="Cantidad",
        required=True,
        widget=forms.NumberInput(attrs={}),
        error_messages={
            "smaller_than_0": "La cantidad ingresada del objeto debe ser mayor a 0."
        },
    )

    description = forms.CharField(
        label="Descripción", required=False, widget=forms.Textarea(attrs={})
    )

    group = forms.ModelChoiceField(
        queryset=None,
        label="Grupo",
        widget=forms.Select(attrs={}),
        error_messages={
            "invalid": "Este groupo no pertenerce al usuario referenciado."
        },
    )

    in_charge = forms.ModelChoiceField(
        queryset=None,
        label="Encargado",
        widget=forms.Select(attrs={}),
        error_messages={
            "invalid": "Este encargado no pertenece al usuario referenciado."
        },
    )

    image = forms.ImageField(
        label="Imagen", required=False, widget=forms.FileInput(attrs={})
    )

    class Meta:
        model = Objects
        fields = ["name", "stock", "description", "group", "in_charge", "image"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        self.user = user
        super().__init__(*args, **kwargs)
        if user:
            self.fields["group"].queryset = ObjectsGroup.objects.filter(
                user=user, is_active=True
            )
            self.fields["in_charge"].queryset = Subprofile.objects.filter(
                profile=user.profile, is_active=True
            )
            self.fields["in_charge"].initial = (
                self.instance.group.in_charge
                if not isinstance(self.instance, object)
                else None
            )

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 3 or len(name) > 100:
            error = ValidationError(
                self.fields["name"].error_messages["invalid_lenght"],
                code="invalid_lenght",
            )
            self.add_error("name", error)
        if (
            Objects.objects.filter(name=name, user=self.user, is_active=True)
            .exclude(id=self.instance.id)
            .exists()
        ):
            error = ValidationError(
                self.fields["name"].error_messages["unique"], code="unique"
            )
            self.add_error("name", error)
        return name

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        stock = int(stock)
        if stock < 1:
            error = ValidationError(
                self.fields["stock"].error_messages["smaller_than_0"],
                code="smaller_than_0",
            )
            self.add_error("stock", error)
        return stock

    def clean_group(self):
        group = self.cleaned_data.get("group")
        if group.user != self.user:
            error = ValidationError(
                self.fields["group"].error_messages["invalid"], code="invalid"
            )

            self.add_error("group", error)
        return group

    def clean_in_charge(self):
        in_charge = self.cleaned_data.get("in_charge")
        if in_charge.profile.user != self.user:
            error = ValidationError(
                self.fields["in_charge"].error_messages["invalid"], code="invalid"
            )
            self.add_error("in_charge", error)
        return in_charge


class ObjectsGroupForm(forms.ModelForm):
    name = forms.CharField(
        label="Nombre",
        required=True,
        widget=forms.TextInput(attrs={}),
        error_messages={
            "invalid_lenght": "El nombre es muy corto o muy largo.",
            "unique": "El nombre del grupo solo puede estar registrado una sola vez.",
        },
    )

    image = forms.ImageField(
        label="Imagen", required=False, widget=forms.FileInput(attrs={})
    )

    description = forms.CharField(
        label="Descripción", required=False, widget=forms.Textarea(attrs={})
    )

    in_charge = forms.ModelChoiceField(
        queryset=None,
        label="Encargado",
        widget=forms.Select(attrs={"id": "in_charge_id"}),
        error_messages={
            "invalid": "Este encargado no pertenece al usuario referenciado."
        },
    )

    class Meta:
        model = ObjectsGroup
        fields = ["name", "image", "in_charge", "description"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        self.user = user
        super().__init__(*args, **kwargs)
        if user:
            self.fields["in_charge"].queryset = Subprofile.objects.filter(
                profile=user.profile, is_active=True
            )

    def clean_in_charge(self):
        in_charge = self.cleaned_data.get("in_charge")
        if in_charge.profile != self.user.profile:
            error = ValidationError(
                self.fields["in_charge"].error_messages["invalid"], code="invalid"
            )
            self.add_error("in_charge", error)
        return in_charge

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 3 or len(name) > 100:
            error = ValidationError(
                self.fields["name"].error_messages["invalid_lenght"],
                code="invalid_lenght",
            )
            self.add_error("name", error)
        if ObjectsGroup.objects.filter(name=name, user=self.user, is_active=True).exclude(
            pk=self.instance.pk
        ):
            error = ValidationError(
                self.fields["name"].error_messages["unique"], code="unique"
            )
            self.add_error("name", error)
        return name


class ExportLogForm(forms.Form):
    start_date = forms.DateField(
        label="Fecha de inicio",
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    end_date = forms.DateField(
        label="Fecha de fin",
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date > end_date:
                error = ValidationError(
                    "La fecha de inicio no puede ser mayor a la fecha de fin.",
                    code="invalid_date_range",
                )
                self.add_error("start_date", error)
