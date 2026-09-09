from django.urls import path

from . import views

app_name = "accounts-api"

urlpatterns = [
    path("registeration/", views.RegistrationApiView.as_view(), name="registration"),
    path("token/login/", views.CustomObtainAuthToken.as_view(), name="token-login"),
]
