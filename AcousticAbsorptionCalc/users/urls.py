from django.urls import path

from .views import (
    HomeView,
    LoginView,
    LogoutView,
    PasswordResetRequestView,
    RegisterView,
    UserProfileUpdateView,
)

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/edit/", UserProfileUpdateView.as_view(), name="edit_profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("home", HomeView.as_view(), name="home"),
    path(
        "password-reset/",
        PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
]
