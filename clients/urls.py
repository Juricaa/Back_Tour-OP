from django.urls import path
from clients import services


urlpatterns = [
    path('', services.client_list, name='client-list'),
    path('<str:pk>/', services.client_detail, name='client-detail'),
]
