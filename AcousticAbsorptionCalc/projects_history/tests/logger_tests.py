from django.test import TestCase
from projects_history.log_change import ChangeLog
from projects_history.Logger import Logger
from users.models import User


class LoggerTests(TestCase):
    def setUp(self):
        self.creator = User.objects.create(username="admin")
        self.user = User.objects.create(username="user")

    def test_log_account_creation_creates_changelog_entry(self):
        Logger.log_account_creation(user_id=self.user.id, changed_by=self.creator)

        log = ChangeLog.objects.last()
        self.assertIsNotNone(log)
        self.assertEqual(log.entity_type, "konto")
        self.assertEqual(log.change_type, "Utworzono konto")
        self.assertEqual(log.entity_id, self.user.id)
        self.assertEqual(log.changed_by, self.creator)
