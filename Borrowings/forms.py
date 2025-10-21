from django import forms
from .models import Borrowings
from Objects.models import Objects
from Users.models import Subprofile
from Users.forms import RequiredLabelMixin


class BorrowingForm(RequiredLabelMixin,forms.ModelForm):
    object = forms.ModelChoiceField(
        label="Objeto", queryset=None, widget=forms.Select()
    )
    in_charge = forms.ModelChoiceField(
        label="Encargado", queryset=None, widget=forms.Select()
    )
    date_limit = forms.DateTimeField(
        label="Fecha límite",
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            }
        ),
    )
    stock = forms.IntegerField(
        label="Cantidad",
        widget=forms.NumberInput(
            attrs={"placeholder": "Cantidad a prestar", "class": "input-field"}
        ),
        error_messages={
            "invalid_stock": "La cantidad solicitada no se encuentra disponible"
        },
    )

    class Meta:
        model = Borrowings
        fields = ["object", "in_charge", "date_limit", "stock"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        self.user = user
        super().__init__(*args, **kwargs)
        if user:
            self.fields["object"].queryset = Objects.objects.filter(
                user=user, stock__gt=0, is_active=True
            )
            self.fields["in_charge"].queryset = Subprofile.objects.filter(
                profile=user.profile, is_active=True
            )

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        object = self.cleaned_data.get("object")
        available = object.available_stock(
            excluded_borrowing=self.instance if self.instance else None
        )
        if stock > available :
            raise forms.ValidationError(f'Solo hay {object.available_stock()} unidades más disponibles.')
        if stock <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a 0')
        return stock
            
