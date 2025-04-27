from typing import Any

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import UpdateView
from django.views.generic.edit import FormView
from projects_history.Logger import Logger

from .forms import (
    PasswordResetRequestForm,
    SetNewPasswordForm,
    UserProfileForm,
    UserRegistrationForm,
)
from .models import PasswordResetToken, User
from .services import AuthService, PasswordResetService, UserService


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("login")

    ACCOUNT_CREATED_MSG = _("Konto utworzone dla {username}")
    ACCOUNT_CREATION_ERROR_MSG = _(
        "Błąd podczas tworzenia konta. Sprawdź poprawność formularza."
    )

    def form_valid(self, form: UserRegistrationForm) -> HttpResponse:
        user = UserService.register_user(form)
        Logger.log_account_creation(user_id=user.id, changed_by=user)
        messages.success(
            self.request, self.ACCOUNT_CREATED_MSG.format(username=user.username)
        )
        return super().form_valid(form)

    def form_invalid(self, form: UserRegistrationForm) -> HttpResponse:
        messages.error(self.request, self.ACCOUNT_CREATION_ERROR_MSG)
        return self.render_to_response(self.get_context_data(form=form))


class LoginView(View):
    INVALID_LOGIN_MSG = _("Nieprawidłowa nazwa użytkownika / email lub hasło")

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "users/login.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")

        user = AuthService.authenticate(identifier, password)
        if user:
            login(request, user)
            return redirect("users:home")
        else:
            messages.error(request, self.INVALID_LOGIN_MSG)
            return render(
                request, "users/login.html", {"error": self.INVALID_LOGIN_MSG}
            )


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy("profile_success")

    PROFILE_UPDATED_MSG = _("Twój profil został zaktualizowany.")
    PROFILE_UPDATE_ERROR_MSG = _("Błąd w formularzu. Spróbuj ponownie.")

    def get_object(self, queryset=None) -> User:
        return self.request.user

    def form_valid(self, form: UserProfileForm) -> HttpResponse:
        UserService.update_user(self.request.user, form.cleaned_data)
        messages.success(self.request, self.PROFILE_UPDATED_MSG)
        return super().form_valid(form)

    def form_invalid(self, form: UserProfileForm) -> HttpResponse:
        messages.error(self.request, self.PROFILE_UPDATE_ERROR_MSG)
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(View):
    LOGOUT_SUCCESS_MSG = _("Zostałeś wylogowany pomyślnie.")

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        UserService.logout_user(request)
        messages.success(request, self.LOGOUT_SUCCESS_MSG)
        return redirect(reverse_lazy("login"))


class HomeView(LoginRequiredMixin, View):
    login_url = "login"
    redirect_field_name = "next"

    def get(self, request):
        return render(request, "home.html")


class PasswordResetRequestView(FormView):
    template_name = "users/password_reset_request.html"
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy("login")

    PASSWORD_RESET_EMAIL_SENT_MSG = _(
        "Jeśli konto istnieje, wysłaliśmy instrukcje resetu hasła na podany adres email."
    )
    PASSWORD_RESET_ERROR_MSG = _("Wystąpił błąd. Spróbuj ponownie później.")

    def form_valid(self, form: PasswordResetRequestForm) -> HttpResponse:
        email = form.cleaned_data["email"]
        success = PasswordResetService.initiate_password_reset(email)

        if success:
            messages.success(self.request, self.PASSWORD_RESET_EMAIL_SENT_MSG)
        else:
            messages.success(self.request, self.PASSWORD_RESET_EMAIL_SENT_MSG)

        return super().form_valid(form)

    def form_invalid(self, form: PasswordResetRequestForm) -> HttpResponse:
        messages.error(self.request, self.PASSWORD_RESET_ERROR_MSG)
        return self.render_to_response(self.get_context_data(form=form))


class PasswordResetConfirmView(FormView):
    template_name = "users/password_reset_confirm.html"
    form_class = SetNewPasswordForm
    success_url = reverse_lazy("login")

    PASSWORD_RESET_SUCCESS_MSG = _(
        "Twoje hasło zostało zmienione. Możesz się teraz zalogować."
    )
    PASSWORD_RESET_ERROR_MSG = _("Token resetu hasła jest nieprawidłowy lub wygasł.")

    def dispatch(self, request, *args, **kwargs):
        self.token = kwargs.get("token")
        self.user = PasswordResetService.validate_token(self.token)

        if not self.user:
            messages.error(self.request, self.PASSWORD_RESET_ERROR_MSG)
            return redirect("password_reset_request")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: SetNewPasswordForm) -> HttpResponse:
        PasswordResetService.reset_password(self.user, form.cleaned_data["password"])
        messages.success(self.request, self.PASSWORD_RESET_SUCCESS_MSG)
        PasswordResetToken.objects.filter(user=self.user).delete()
        return super().form_valid(form)
