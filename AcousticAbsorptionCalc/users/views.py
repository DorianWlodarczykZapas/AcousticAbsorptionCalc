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

from .forms import UserProfileForm, UserRegistrationForm
from .models import User
from .services import AuthService, UserService


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
    def post(self, request, *args, **kwargs):
        UserService.logout_user(request)
        messages.success(request, "Zostałeś wylogowany pomyślnie.")
        return redirect(reverse_lazy("login"))


class HomeView(LoginRequiredMixin, View):
    login_url = "login"
    redirect_field_name = "next"

    def get(self, request):
        return render(request, "home.html")
