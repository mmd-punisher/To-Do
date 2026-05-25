from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import RegisterView, CustomLoginView, CustomLogoutView, ProfileView

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
]
