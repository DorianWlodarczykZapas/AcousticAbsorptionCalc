from django import forms

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
