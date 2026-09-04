from django.contrib.auth.decorators import login_required
from django.urls import include, path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    HomeView,
    ProfileUpdateView,
    ProfileView,
    RegisterView,
)

app_name = "accounts"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", login_required(ProfileView.as_view()), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="edit_profile"),
    path("api/v1/", include("accounts.api.v1.urls")),
]
