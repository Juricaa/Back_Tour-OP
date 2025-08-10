# accounts/urls.py
from django.urls import path
from . import services

urlpatterns = [
    path('register/', services.RegisterSecretaireView.as_view(), name='register_secretaire'),
    path('login/', services.LoginView.as_view(), name='login'),
]
