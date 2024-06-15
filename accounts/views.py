from django.contrib.auth import get_user
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .forms import UserLoginForm

class LoginView(BaseLoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

class LogoutView(BaseLogoutView):
    template_name = 'accounts/login.html'
    redirect_field_name = 'next'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    
class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user(self.request)
        context['user'] = user
        return context