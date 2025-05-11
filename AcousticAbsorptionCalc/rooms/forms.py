from django import forms
from django.forms import formset_factory
from django.utils.translation import gettext_lazy as _

from .models import Material, Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "width", "length", "height", "norm"]
        labels = {
            "name": _("Room Name"),
            "width": _("Width (m)"),
            "length": _("Length (m)"),
            "height": _("Height (m)"),
            "norm": _("Acoustic Norm"),
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "width": forms.NumberInput(attrs={"class": "form-control"}),
            "length": forms.NumberInput(attrs={"class": "form-control"}),
            "height": forms.NumberInput(attrs={"class": "form-control"}),
            "norm": forms.Select(attrs={"class": "form-control"}),
        }


class FurnishingForm(forms.Form):
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        label=_("Material"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    area = forms.FloatField(
        label=_("Area (m²)"),
        min_value=0.01,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )


FurnishingFormSet = formset_factory(FurnishingForm, extra=1, can_delete=True)
