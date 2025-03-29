from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from projects_history.Logger import Logger

from .forms import UserRegistrationForm


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users/home.html")  

    def form_valid(self, form):
        user = form.save()

        Logger.log_account_creation(user_id=user.id, changed_by=user)

        messages.success(self.request, f"Konto utworzone dla {user.username}")
        return super().form_valid(form)

