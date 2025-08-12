# accounts/urls.py
from django.urls import path
from . import services
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', services.RegisterSecretaireView.as_view(), name='register_secretaire'),
    path('login/', services.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', services.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', services.UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/verify/', services.verify_user, name='verify-user'),
]
