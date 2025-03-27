from django.contrib import messages
from django.shortcuts import redirect, render
from projects_history import Logger

from .forms import UserRegistrationForm


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            Logger.log_account_creation(user_id=user.id, changed_by=user)

            messages.success(request, f"Konto utworzone dla {user.username}")
            return redirect("sth")
    else:
        form = UserRegistrationForm()

    return render(request, "users/register.html", {"form": form})
