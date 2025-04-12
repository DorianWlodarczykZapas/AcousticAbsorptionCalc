from django.contrib.auth import logout
from django.utils.timezone import now, timedelta
from .models import User
from .repositories import UserRepository
from plans.models import Plan


class AuthService:
    @staticmethod
    def authenticate(identifier, password):
        user = UserRepository.get_by_identifier(identifier)
        if user and user.check_password(password):
            return user
        return None


class UserService:
    @staticmethod
    def register_user(form):
        user = form.save()

        try:
            trial_plan = Plan.objects.get(type=Plan.PlanType.TRIAL)
        except Plan.DoesNotExist:
            raise Exception("Plan Trial nie został znaleziony. Upewnij się, że istnieje w bazie.")

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
    def update_user(user: User, data: dict):
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)

        new_password = data.get("new_password")
        if new_password:
            user.set_password(new_password)

        user.save()

    @staticmethod
    def logout_user(request):
        logout(request)
