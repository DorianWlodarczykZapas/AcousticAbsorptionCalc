from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.db import models
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from projects_history.Logger import Logger

from .forms import UserRegistrationForm
from .models import User


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users/home.html")

    def form_valid(self, form):
        user = form.save()

        Logger.log_account_creation(user_id=user.id, changed_by=user)

        messages.success(self.request, f"Konto utworzone dla {user.username}")
        return super().form_valid(form)


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")

        user = User.objects.filter(
            models.Q(username=identifier) | models.Q(email=identifier)
        ).first()

        if user and check_password(password, user.password_hash):
            request.session["user_id"] = user.id
            request.user = user
            return redirect("home")
        else:
            messages.error(request, "Invalid username/email or password")
            return render(request, "login.html", {"error": "Invalid credentials"})
