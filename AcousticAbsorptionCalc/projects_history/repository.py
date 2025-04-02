from .models import ChangeLog


class ChangeLogRepository:
    @staticmethod
    def get_logs_by_user(user):
        return ChangeLog.objects.filter(changed_by=user).order_by("-timestamp")
