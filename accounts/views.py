from django.shortcuts import render
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserLoginForm
from django.views.generic import TemplateView

class LoginView(BaseLoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

class LogoutView(BaseLogoutView):
    template_name = 'accounts/login.html'
    redirect_field_name = 'next'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
