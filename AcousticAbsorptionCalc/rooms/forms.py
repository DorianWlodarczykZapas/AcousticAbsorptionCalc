from django import forms
from django.forms import formset_factory, modelformset_factory
from django.utils.translation import gettext_lazy as _

from .models import Material, Room, RoomSurface


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
            "area": _("Area (m²)"),
        }
        widgets = {
            "surface_type": forms.Select(attrs={"class": "form-control"}),
            "material": forms.Select(attrs={"class": "form-control"}),
            "area": forms.NumberInput(attrs={"class": "form-control"}),
        }


RoomSurfaceFormSet = modelformset_factory(
    RoomSurface, form=RoomSurfaceForm, extra=1, can_delete=True
)


class FurnishingForm(forms.Form):
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        label=_("Material"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    area = forms.FloatField(
        label=_("Area (m²) / Quantity"),
        min_value=0.01,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )


FurnishingFormSet = formset_factory(FurnishingForm, extra=1, can_delete=True)
