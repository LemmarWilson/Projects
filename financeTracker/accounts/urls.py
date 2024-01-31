from django.urls import path
from .views import (
    UserRegistrationView,
    UserDashboardView
)

app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
]
