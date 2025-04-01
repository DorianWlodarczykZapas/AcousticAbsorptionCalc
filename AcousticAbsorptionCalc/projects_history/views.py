from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import ChangeLog


class UserChangeLogListView(LoginRequiredMixin, ListView):
    model = ChangeLog
    template_name = "changelog/user_logs.html"
    context_object_name = "logs"
    paginate_by = 25

    def get_queryset(self):
        return ChangeLog.objects.filter(changed_by=self.request.user).order_by(
            "-timestamp"
        )
