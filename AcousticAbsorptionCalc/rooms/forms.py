from django import forms
from django.forms import formset_factory, modelformset_factory
from django.utils.translation import gettext_lazy as _

from .models import Furnishing, Room, RoomSurface


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "width", "length", "height", "norm", "project"]
        labels = {
            "name": _("Room Name"),
            "width": _("Width (m)"),
            "length": _("Length (m)"),
            "height": _("Height (m)"),
            "norm": _("Acoustic Norm"),
            "project": _("Project (optional)"),
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "width": forms.NumberInput(attrs={"class": "form-control"}),
            "length": forms.NumberInput(attrs={"class": "form-control"}),
            "height": forms.NumberInput(attrs={"class": "form-control"}),
            "norm": forms.Select(attrs={"class": "form-control"}),
            "project": forms.Select(attrs={"class": "form-control"}),
        }


class RoomSurfaceForm(forms.ModelForm):
    class Meta:
        model = RoomSurface
        fields = ["surface_type", "material", "area"]
        labels = {
            "surface_type": _("Surface Type"),
            "material": _("Material"),
            "area": _("Area (m²) / Quantity:"),
        }
        widgets = {
            "surface_type": forms.Select(attrs={"class": "form-control"}),
            "material": forms.Select(attrs={"class": "form-control"}),
            "area": forms.NumberInput(attrs={"class": "form-control"}),
        }


RoomSurfaceFormSet = modelformset_factory(
    RoomSurface, form=RoomSurfaceForm, extra=1, can_delete=True
)


class FurnishingForm(forms.ModelForm):
    class Meta:
        model = Furnishing
        fields = ["material", "quantity"]
        labels = {
            "material": _("Material"),
            "quantity": _("Area (m²) / Quantity:"),
        }
        widgets = {
            "material": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        }


FurnishingFormSet = formset_factory(FurnishingForm, extra=1, can_delete=True)
