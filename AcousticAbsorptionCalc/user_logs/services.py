from .repository import ChangeLogRepository


class ChangeLogService:
    @staticmethod
    def get_user_logs(user):
        return ChangeLogRepository.get_logs_by_user(user)
