from unittest.mock import patch

from django.test import TestCase
from projects_history.log_change import ChangeLog, log_change
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

    def test_log_account_creation_raises_when_user_does_not_exist(self):
        non_existing_id = 9999
        with self.assertRaises(User.DoesNotExist):
            Logger.log_account_creation(
                user_id=non_existing_id, changed_by=self.creator
            )

    def test_log_account_creation_missing_changed_by_does_not_log(self):
        Logger.log_account_creation(user_id=self.user.id, changed_by=None)
        self.assertIsNone(ChangeLog.objects.last())

    def test_log_account_creation_missing_user_id_does_not_log(self):
        Logger.log_account_creation(user_id=None, changed_by=self.creator)
        self.assertIsNone(ChangeLog.objects.last())

    def test_log_room_created_creates_changelog(self):
        Logger.log_room_created(user_id=self.user.id, changed_by=self.creator)

        log = ChangeLog.objects.last()
        self.assertEqual(log.entity_type, "pomieszczenie")
        self.assertEqual(log.change_type, "Dodano")
        self.assertEqual(log.entity_id, self.user.id)
        self.assertEqual(log.changed_by, self.creator)

    @patch("logger.log_change.ChangeLog.objects.create")
    def test_log_account_creation_calls_changelog_create(self, mock_create):
        Logger.log_account_creation(user_id=self.user.id, changed_by=self.creator)
        mock_create.assert_called_once()

    def test_decorator_preserves_function_return_value(self):
        @log_change(entity_type="test", change_type="typ")
        def dummy_func(user_id, changed_by):
            return "ok"

        result = dummy_func(user_id=self.user.id, changed_by=self.creator)
        self.assertEqual(result, "ok")

    def test_decorator_does_not_log_without_required_args(self):
        @log_change(entity_type="test", change_type="typ")
        def dummy_func(user_id=None, changed_by=None):
            return "ok"

        result = dummy_func()
        self.assertEqual(result, "ok")
        self.assertIsNone(ChangeLog.objects.last())
