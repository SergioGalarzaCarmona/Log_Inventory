from django import forms
from .models import Borrowings
from Objects.models import Objects
from Users.models import Subprofile


class BorrowingForm(forms.ModelForm):
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
