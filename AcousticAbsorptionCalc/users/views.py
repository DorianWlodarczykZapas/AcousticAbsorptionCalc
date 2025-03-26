from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        return render(request, "users/register.html", {"form": form})
