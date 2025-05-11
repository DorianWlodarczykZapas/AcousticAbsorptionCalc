from calculations.models import Material
from django import forms
from django.forms import formset_factory

from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "width", "length", "height", "norm"]
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
        label="Material",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    area = forms.FloatField(
        label="Area (m²)",
        min_value=0.01,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )


FurnishingFormSet = formset_factory(FurnishingForm, extra=1, can_delete=True)
