from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views import View


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "app_title": _("Acoustic Absorption Calculator"),
            "description": _(
                "A web application to calculate the acoustic absorption of rooms based on materials and geometry."
            ),
            "login_text": _("Log In"),
            "register_text": _("Register"),
        }
        return render(request, "calculations/home.html", context)
