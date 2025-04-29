from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"
    extra_context = {
        "title": _("Acoustic Absorption Calculator"),
        "description": _("Easily calculate and manage sound absorption projects."),
        "login_text": _("Log in"),
        "register_text": _("Register"),
    }
