from typing import Any

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import User


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        min_length=8,
        help_text=_("Password must be at least 8 characters long."),
    )
    password2 = forms.CharField(
        label=_("Repeat password"),
        widget=forms.PasswordInput,
        min_length=8,
    )
    email = forms.EmailField(
        required=True,
        help_text=_("Enter a valid email address."),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": _("Username"),
            "email": _("Email address"),
        }

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords must match."))

        return cleaned_data

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.role = "free_version"

        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    new_password = forms.CharField(
        label=_("New password"),
        max_length=255,
        required=False,
        widget=forms.PasswordInput,
        help_text=_("Leave empty if you don't want to change the password."),
    )

    class Meta:
        model = User
        fields = ["username", "email", "new_password"]
        labels = {
            "username": _("Username"),
            "email": _("Email address"),
        }

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")

        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()
        return user


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)


class SetNewPasswordForm(forms.Form):
    password = forms.CharField(label=_("New password"), widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        label=_("Confirm new password"), widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(_("Passwords must match."))
        return cleaned_data
