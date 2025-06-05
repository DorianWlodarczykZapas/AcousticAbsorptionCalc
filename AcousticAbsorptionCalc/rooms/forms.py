from django import forms
from django.forms import formset_factory, modelformset_factory
from django.utils.translation import gettext_lazy as _
from projects.models import Project

from .models import Material, Room, RoomMaterial


class RoomForm(forms.ModelForm):
    floor_material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        label=_("Floor material"),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )
    ceiling_material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        label=_("Ceiling material"),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )
    wall_a_material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        label=_("Wall A material"),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )
    wall_b_material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        label=_("Wall B material"),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )
    wall_c_material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        label=_("Wall C material"),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )
    wall_d_material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        label=_("Wall D material"),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )

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


FurnishingFormSet = formset_factory(FurnishingForm, extra=0, can_delete=True)


class MoveRoomForm(forms.Form):
    target_project = forms.ModelChoiceField(
        queryset=None, label=_("Select target project")
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["target_project"].queryset = Project.objects.filter(members=user)


class RoomMaterialForm(forms.ModelForm):
    class Meta:
        model = RoomMaterial
        fields = ["material", "location"]
        labels = {
            "material": _("Material"),
            "location": _("Location"),
        }
        widgets = {
            "material": forms.Select(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
        }


RoomMaterialFormSet = modelformset_factory(
    RoomMaterial,
    form=RoomMaterialForm,
    extra=1,
    can_delete=True,
)
