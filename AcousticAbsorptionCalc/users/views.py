from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
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

    def form_valid(self, form):
        user = UserService.register_user(form)
        Logger.log_account_creation(user_id=user.id, changed_by=user)
        messages.success(self.request, f"Konto utworzone dla {user.username}")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            _("Błąd podczas tworzenia konta. Sprawdź poprawność formularza."),
        )
        return self.render_to_response(self.get_context_data(form=form))


class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")

        user = AuthService.authenticate(identifier, password)
        if user:
            login(request, user)
            return redirect("users:home")
        else:
            messages.error(request, "Nieprawidłowa nazwa użytkownika / email lub hasło")
            return render(
                request, "users/login.html", {"error": "Nieprawidłowe dane logowania"}
            )


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy("profile_success")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        UserService.update_user(self.request.user, form.cleaned_data)
        messages.success(self.request, "Twój profil został zaktualizowany.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Błąd w formularzu. Spróbuj ponownie.")
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
