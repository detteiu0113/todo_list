from django.urls import path
from .views import LoginView, LogoutView, DashboardView, UserProfileView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('profile/', UserProfileView.as_view(), name='user_profile')
]