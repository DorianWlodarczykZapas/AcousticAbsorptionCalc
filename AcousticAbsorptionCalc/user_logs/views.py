from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .services import ChangeLogService


class UserChangeLogListView(LoginRequiredMixin, ListView):
    template_name = "user_logs/user_logs.html"
    context_object_name = "logs"
    paginate_by = 25

    def get_queryset(self):
        return ChangeLogService.get_user_logs(self.request.user)
