from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "app_title": _("Acoustic Absorption Calculator"),
                "description": _(
                    "Easily calculate and manage sound absorption projects."
                ),
                "login_text": _("Log in"),
                "register_text": _("Register"),
            }
        )
        return context
