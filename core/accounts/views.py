from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegisterForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register_page.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()

        login(self.request, user)
        messages.success(self.request, f'Welcome {user.username}.')

        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Error in registration, check your data.')
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    template_name = 'accounts/login_page.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('accounts:profile')

    def form_valid(self, form):
        messages.success(self.request, f'Welcome {self.request.user.username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Username or password is incorrect.')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Logout.')
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginView):
    template_name = 'accounts/profile_page.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)