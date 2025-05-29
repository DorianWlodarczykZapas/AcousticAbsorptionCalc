import uuid
from typing import Dict, Optional

from django.conf import settings
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.timezone import now, timedelta
from django.utils.translation import gettext_lazy as _
from plans.models import Plan, UserPlan
from user_logs.logger import Logger

from .models import PasswordResetToken, User
from .repositories import UserRepository


class AuthService:
    @staticmethod
    def authenticate(identifier: str, password: str) -> Optional[User]:
        user = UserRepository.get_by_identifier(identifier)
        if user and user.check_password(password):
            return user
        return None


class UserService:
    @staticmethod
    def register_user(form) -> User:
        user = form.save()

        trial_plan, _ = Plan.objects.get_or_create(
            type=Plan.PlanType.TRIAL,
            defaults={
                "name": "Trial Plan",
                "description": ("Default trial plan"),
                "price": 0.00,
                "billing_period": "7 days",
                "max_projects": 1,
                "max_rooms_per_project": 5,
                "advanced_features_enabled": False,
            },
        )

        UserPlan.objects.create(
            user=user,
            plan=trial_plan,
            start_date=now().date(),
            valid_to=now().date() + timedelta(days=7),
            is_trial=True,
            trial_days=7,
        )

        return user

    @staticmethod
    def update_user(user: User, data: Dict[str, str]) -> None:
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)

        new_password = data.get("new_password")
        if new_password:
            user.set_password(new_password)

        user.save()

    @staticmethod
    def logout_user(request) -> None:
        logout(request)


class PasswordResetService:
    @staticmethod
    def initiate_password_reset(email: str) -> bool:
        try:
            user = User.objects.get(email=email)
            reset_token = PasswordResetToken.objects.create(user=user)
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{reset_token.token}"

            subject = _("Password reset")
            message = render_to_string(
                "emails/password_reset_email.html", {"reset_link": reset_link}
            )
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            Logger.log_password_reset_requested(user_id=user.id, changed_by=user)

            return True
        except User.DoesNotExist:
            return False

    @staticmethod
    def validate_token(token: str) -> User | None:
        try:
            uuid_token = uuid.UUID(token)
            reset_token = PasswordResetToken.objects.get(token=uuid_token)
            if reset_token.is_expired():
                reset_token.delete()
                return None
            return reset_token.user
        except (PasswordResetToken.DoesNotExist, ValueError):
            return None

    @staticmethod
    def reset_password(user: User, new_password: str) -> None:
        user.set_password(new_password)
        user.save()
        Logger.log_password_reset(user_id=user.id, changed_by=user)
