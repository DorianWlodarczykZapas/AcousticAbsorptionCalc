from django.urls import path

from .views import LoginView, RegisterView, UserProfileUpdateView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/edit/", UserProfileUpdateView.as_view(), name="edit_profile"),
]
