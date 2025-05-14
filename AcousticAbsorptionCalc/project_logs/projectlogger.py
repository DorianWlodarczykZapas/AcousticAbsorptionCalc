from .log_project_change import log_project_change
from .models import ProjectChangeLog


class ProjectLogger:
    """Logger for project-related actions."""

    @staticmethod
    @log_project_change(change_type=ProjectChangeLog.ChangeType.CREATED)
    def log_created(project, changed_by):
        pass

    @staticmethod
    @log_project_change(change_type=ProjectChangeLog.ChangeType.DELETED)
    def log_deleted(project, changed_by):
        pass

    @staticmethod
    @log_project_change(change_type=ProjectChangeLog.ChangeType.SHARED)
    def log_shared(project, changed_by, change_description="", metadata=None):
        pass

    @staticmethod
    @log_project_change(change_type=ProjectChangeLog.ChangeType.DOWNLOADED)
    def log_downloaded(project, changed_by, change_description="", metadata=None):
        pass

    @staticmethod
    @log_project_change(change_type=ProjectChangeLog.ChangeType.EDIT_DIMENSIONS)
    def log_edit_dimensions(project, changed_by, change_description="", metadata=None):
        pass

    @staticmethod
    @log_project_change(change_type=ProjectChangeLog.ChangeType.EDIT_FURNISHING)
    def log_edit_furnishing(project, changed_by, change_description="", metadata=None):
        pass

    @staticmethod
    @log_project_change(change_type=ProjectChangeLog.ChangeType.EDIT_STANDARD)
    def log_edit_standard(project, changed_by, change_description="", metadata=None):
        pass
