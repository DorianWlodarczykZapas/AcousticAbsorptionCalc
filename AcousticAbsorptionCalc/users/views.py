from typing import Any, Dict

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
from plans.models import UserPlan
from projects.models import Project
from rooms.models import Room
from user_logs.logger import Logger

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
    success_url = reverse_lazy("users:login")

    def form_valid(self, form: UserRegistrationForm) -> HttpResponse:
        user = UserService.register_user(form)
        Logger.log_account_creation(user_id=user.id, changed_by=user)
        messages.success(
            self.request,
            _("Account created for {username}").format(username=user.username),
        )
        return super().form_valid(form)

    def form_invalid(self, form: UserRegistrationForm) -> HttpResponse:
        messages.error(
            self.request,
            _("Error while creating account. Please check the form."),
        )
        return self.render_to_response(self.get_context_data(form=form))


class LoginView(View):
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
            error_msg = _("Invalid username/email or password")
            messages.error(request, error_msg)
            return render(request, "users/login.html")


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None) -> User:
        return self.request.user

    def form_valid(self, form: UserProfileForm) -> HttpResponse:
        UserService.update_user(self.request.user, form.cleaned_data)
        messages.success(self.request, _("Your profile has been updated."))
        return super().form_valid(form)

    def form_invalid(self, form: UserProfileForm) -> HttpResponse:
        messages.error(
            self.request, _("There was an error in the form. Please try again.")
        )
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(View):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        UserService.logout_user(request)
        messages.success(request, _("You have been successfully logged out."))
        return redirect(reverse_lazy("users:login"))


class HomeView(LoginRequiredMixin, View):
    login_url = "login"
    redirect_field_name = "next"

    def get(self, request, *args: Any, **kwargs: Any) -> Any:
        user = request.user

        latest_project = (
            Project.objects.filter(user=user).order_by("-created_at").first()
        )

        latest_room = (
            Room.objects.filter(project__user=user).order_by("-created_at").first()
        )

        active_user_plan = (
            UserPlan.objects.select_related("plan")
            .filter(user=user, is_active=True)
            .first()
        )

        plan_data = None
        if active_user_plan:
            plan_data = {
                "name": active_user_plan.plan.name,
                "type": active_user_plan.plan.get_type_display(),
                "valid_to": active_user_plan.valid_to,
                "advanced_features": active_user_plan.plan.advanced_features_enabled,
                "max_projects": active_user_plan.plan.max_projects,
                "max_rooms": active_user_plan.plan.max_rooms_per_project,
            }

        context: Dict[str, Any] = {
            "latest_project": latest_project,
            "latest_room": latest_room,
            "active_user_plan": active_user_plan,
            "plan_data": plan_data,
        }

        return render(request, "users/main_page.html", context)


class PasswordResetRequestView(FormView):
    template_name = "users/password_reset_request.html"
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy("login")

    def form_valid(self, form: PasswordResetRequestForm) -> HttpResponse:
        email = form.cleaned_data["email"]
        PasswordResetService.initiate_password_reset(email)

        messages.success(
            self.request,
            _(
                "If the account exists, we've sent password reset instructions to the provided email."
            ),
        )
        return super().form_valid(form)

    def form_invalid(self, form: PasswordResetRequestForm) -> HttpResponse:
        messages.error(self.request, _("An error occurred. Please try again later."))
        return self.render_to_response(self.get_context_data(form=form))


class PasswordResetConfirmView(FormView):
    template_name = "users/password_reset_confirm.html"
    form_class = SetNewPasswordForm
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        self.token = kwargs.get("token")
        self.user = PasswordResetService.validate_token(self.token)

        if not self.user:
            messages.error(
                request, _("The password reset token is invalid or has expired.")
            )
            return redirect("password_reset_request")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: SetNewPasswordForm) -> HttpResponse:
        PasswordResetService.reset_password(self.user, form.cleaned_data["password"])
        messages.success(
            self.request, _("Your password has been changed. You can now log in.")
        )
        PasswordResetToken.objects.filter(user=self.user).delete()
        return super().form_valid(form)

    def form_invalid(self, form: SetNewPasswordForm) -> HttpResponse:
        return self.render_to_response(self.get_context_data(form=form))
