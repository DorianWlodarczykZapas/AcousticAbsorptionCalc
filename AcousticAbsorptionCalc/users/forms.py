from django import forms

from .models import User


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput,
        min_length=8,
        help_text="Hasło musi mieć co najmniej 8 znaków.",
    )
    password2 = forms.CharField(
        label="Powtórz hasło",
        widget=forms.PasswordInput,
        min_length=8,
    )
    email = forms.EmailField(required=True, help_text="Wprowadź poprawny adres e-mail.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła muszą być takie same.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.role = "free_version"

        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):

    new_password = forms.CharField(
        label="Nowe hasło",
        max_length=255,
        required=False,
        widget=forms.PasswordInput,
        help_text="Pozostaw puste, jeśli nie chcesz zmieniać hasła.",
    )

    class Meta:
        model = User
        fields = ["username", "email", "new_password"]

    def clean_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        return new_password if new_password else None
